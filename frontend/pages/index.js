import "regenerator-runtime/runtime";
import React, { useState, useEffect } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import { Container, Spacer, Card, Button, Text, Row } from "@nextui-org/react";

import Head from "next/head";

export default function Home() {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [currentVideo, setCurrentVideo] = useState("base.mp4");
  const [history, setHistory] = useState([
    {
      role: "system",
      content:
        "Du bist der nette Assistent einer älteren Person und du heißt Anna.",
    },
  ]);
  const [listening, setListening] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const pause = 2000;

  useEffect(() => {
    if (transcript !== "" && isMounted) {
      let timeoutId = setTimeout(async () => {
        await setHistory((history) => [
          ...history,
          {
            role: "user",
            content: transcript,
          },
        ]);
        console.log(history);
        // Make a POST request to your backend endpoint here
        fetch("http://localhost:8000/process_input", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            history: [...history, { role: "user", content: transcript }],
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to send transcript to backend.");
            }
            return response.json();
          })
          .then((data) => {
            setHistory((history) => [
              ...history,
              {
                role: "assistant",
                content: data.answer,
              },
            ]);
            console.log(data.video.videoUrl);
            setCurrentVideo(data.video.videoUrl);
            console.log(currentVideo);
          })
          .catch((error) => {
            console.error(error);
          });
        resetTranscript();
      }, pause);

      return () => {
        clearTimeout(timeoutId);
      };
    }
  }, [transcript, history, isMounted, currentVideo]);

  function startListening() {
    SpeechRecognition.startListening({ continuous: true, language: "de-DE" });
    setListening(true);
  }

  function stopListening() {
    SpeechRecognition.abortListening();
    setListening(false);
  }

  function buttonClick() {
    if (listening) {
      stopListening();
    } else {
      startListening();
    }
  }

  function handleVideoEnd() {
    const video = document.getElementById("video-player");
    video.currentTime = 0;
    video.pause();
  }

  return (
    <>
      <Head>
        <link rel="stylesheet" href="https://cdn.plyr.io/3.6.8/plyr.css" />
        <script src="https://cdn.plyr.io/3.6.8/plyr.js"></script>
      </Head>

      <Spacer y={2} />
      <Container xs>
        <Card>
          <Card.Body>
            <video
              id="video-player"
              controls={true}
              autoPlay={true}
              muted={true}
              style={{ width: "100%", height: "auto" }}
              controlsList="mute"
            >
              <source src={currentVideo} type="video/mp4" />
            </video>
            <h2>Hey Anna</h2>
            {history.slice(1).map((item) => (
              <Text blockquote>{item.content}</Text>
            ))}
          </Card.Body>
          <Card.Divider />
          <Card.Footer>
            <Row justify="flex-end">
              <Button
                size="sm"
                light
                onPress={() => {
                  setHistory([]);
                }}
              >
                Reset
              </Button>
              <Button
                size="sm"
                onPress={() => {
                  buttonClick();
                }}
              >
                {listening ? "Stop" : "Start"}
              </Button>
            </Row>
          </Card.Footer>
        </Card>
      </Container>
    </>
  );
}
