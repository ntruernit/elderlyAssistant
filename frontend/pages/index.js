import "regenerator-runtime/runtime";
import React, { useState, useEffect } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import { Container, Spacer, Card, Button, Text, Row } from "@nextui-org/react";

import Head from "next/head";

export default function Home() {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [history, setHistory] = useState([]);
  const [listening, setListening] = useState(false);

  const pause = 2000;

  useEffect(() => {
    if (transcript !== "") {
      let timeoutId = setTimeout(() => {
        setHistory((history) => [
          ...history,
          { role: "user", content: transcript },
        ]);
        resetTranscript();
        console.log(history);
      }, pause);

      return () => {
        clearTimeout(timeoutId);
      };
    }
  }, [transcript]);

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
              loop
              controls={false}
              autoPlay={true}
              muted={true}
              style={{ width: "70%", height: "auto" }}
            >
              <source src="base.webm" type="video/webm" />
            </video>
            <h2>Hey Anna</h2>
            {history.map((item) => (
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
              <Button size="sm" onPress={() => {buttonClick()}}>
                {listening ? "Stop" : "Start"}
              </Button>
            </Row>
          </Card.Footer>
        </Card>
      </Container>
    </>
  );
}
