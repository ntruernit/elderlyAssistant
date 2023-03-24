import "regenerator-runtime/runtime";
import React, { useState, useEffect, useRef } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import { Container, Spacer, Card, Button, Text, Row } from "@nextui-org/react";

import Head from "next/head";

export default function Home() {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [currentVideo, setCurrentVideo] = useState("base.mp4");
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);
  const [initial, setInitial] = useState(true);
  const videoRef = useRef(null);
  const [history, setHistory] = useState([
    {
      role: "system",
      content:
        "Du bist der nette Assistent einer älteren Person und du heißt Anna.",
    },
  ]);
  const [listening, setListening] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const [hasEnded, setHasEnded] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const pause = 2000;

  // CALL the API
  useEffect(() => {
    if (transcript !== "" && isMounted) {
      let timeoutId = setTimeout(async () => {
        stopListening()
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
          .then(async (data) => {
            setHistory((history) => [
              ...history,
              {
                role: "assistant",
                content: data.answer,
              },
            ]);

            await setCurrentVideo(data.video.videoUrl);
            console.log(currentVideo);
            videoRef.current.play();
          })
          .catch((error) => {
            console.error(error);
          });
        resetTranscript();
      }, pause);

      return () => {
        clearTimeout(timeoutId);
        startListening()
      };
    }
  }, [transcript, history, isMounted]);

  useEffect(() => {
    if (currentVideo) {
      setHasEnded(false); // reset hasEnded when video changes
      const timeoutId = setTimeout(() => {
        videoRef.current.src = currentVideo;
        videoRef.current.load();
        videoRef.current.play();
        setIsVideoPlaying(true); // set isVideoPlaying to true when video starts playing
      }, 3000);
      return () => {
        clearTimeout(timeoutId);
        setIsVideoPlaying(false); // set isVideoPlaying to false when video stops playing
        startListening()
      };
    }
  }, [currentVideo]);

  useEffect(() => {
    if (!isVideoPlaying && !initial) {
      console.log(isVideoPlaying);
      startListening();
    } else {
      stopListening();
    }
  }, [isVideoPlaying, initial]);

  useEffect(() => {
    if (hasEnded) {
      console.log("heya");
      startListening();
    }
  }, [hasEnded]);

  function startListening() {
    SpeechRecognition.startListening({ continuous: true, language: "de-DE" });
    setListening(true);
  }

  function stopListening() {
    SpeechRecognition.abortListening();
    setListening(false);
  }

  function buttonClick() {
    if (initial) {
      setInitial(false);
      videoRef.current.play();
      return
    }
    if (listening) {
      stopListening();
    }
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
              ref={videoRef}
              controls={true}
              style={{ width: "100%", height: "auto" }}
              muted={false}
              onEnded={() => {
                setHasEnded(true);
              }}
            >
              <source src={currentVideo} type="video/mp4" />
            </video>
            <h2>Hey Anna</h2>
            {history
              .slice(1)
              .reverse()
              .slice(0, 5)
              .map((item) => (
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
