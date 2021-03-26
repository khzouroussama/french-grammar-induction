import React, { useState } from "react";
import tw, { styled } from "twin.macro";
import TextareaAutosize from "react-autosize-textarea";
import { motion, AnimateSharedLayout } from "framer-motion";

import { AnalyzeResults } from "./Components/AnalyzeResults";

import { ImSpinner9 } from "react-icons/im";
import { SiElectron } from "react-icons/si";
import { IoBarcodeOutline, IoSearchSharp } from "react-icons/io5";

let API =
  process.env.NODE_ENV === "production"
    ? process.env.REACT_APP_PROD_API
    : process.env.REACT_APP_DEV_API;

const Container = tw.div`flex min-h-screen p-2 lg:p-4  bg-gradient-to-tr from-indigo-200 via-pink-100 to-yellow-50`;
const MainContent = tw(motion.div)`w-full flex flex-col`;
const TextInput = tw(
  TextareaAutosize
)`whitespace-pre-wrap border p-3 rounded-3xl border-gray-200
    ring-2 ring-pink-700 text-gray-500 resize-none text-center
     hover:shadow-xl mx-auto w-full lg:w-2/4 outline-none`;
const Button = tw(
  motion.div
)`cursor-pointer flex align-middle rounded-3xl px-6 font-bold h-10 m-3 mx-auto bg-gradient-to-br from-indigo-600 via-pink-600 to-yellow-500 text-white shadow focus:ring-2 focus:ring-yellow-400`;

export const SelectableHalf = styled.div(({ selected, direction }) => [
  tw`w-1/2 h-full bg-gradient-to-br from-indigo-200 via-pink-200 to-yellow-100 hover:bg-gradient-to-tr hover:from-yellow-200 hover:via-pink-300 hover:to-indigo-300 flex text-pink-600 cursor-pointer`,
  selected &&
    tw`bg-gradient-to-br from-indigo-500 via-pink-500 to-yellow-400 hover:bg-gradient-to-tr hover:from-yellow-500 hover:via-pink-600 hover:to-indigo-600  text-yellow-50`,
  direction === "right" ? tw`rounded-r-3xl` : tw`rounded-l-3xl`,
]);

function App() {
  const [sent, setSent] = useState(
    "Elle a aussi plaidé pour une réforme de la procédure pénale pour qu'elle soit adaptée aux articles de la Déclaration Universelle des Droits de l'Homme, sur les droits des prisonniers à comparaître devant un tribunal indépendant et impartial et à disposer de garanties de procédures et de la présomption d'innocence."
  );

  const [corpus, setCorpus] = useState("");
  const [testCorpus, setTestCorpus] = useState("");

  const [selectedModel, setSelectedModel] = useState(1);
  const [result, setResult] = useState(undefined);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeText = () => {
    setLoading(true);
    setResult(undefined);

    fetch(`${API}/analyze?sent=${sent}`)
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch((e) => {
        alert("Error");
        setLoading(false);
      });
  };

  const handleGenerateGrammar = () => {
    setLoading(true);
    setResult(undefined);

    console.log(JSON.stringify(testCorpus));

    fetch(
      `${API}/generate?corpus=${corpus.replaceAll(
        "\n",
        "$"
      )}&test=${testCorpus.replaceAll("\n", "$")}`
    )
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch((e) => {
        alert("Error");
        setLoading(false);
      });
  };

  return (
    <AnimateSharedLayout>
      <Container>
        <MainContent>
          <motion.div layout tw="flex flex-col my-auto w-full">
            <motion.div
              key={selectedModel}
              animate={{ opacity: [0, 1], y: [20, 0] }}
              transition={{ duration: 0.3 }}
            >
              <motion.div animate={{ opacity: [0, 1], y: [-20, 0] }}>
                {selectedModel === 2 ? (
                  <SiElectron tw="mx-auto text-7xl text-pink-600" />
                ) : (
                  <IoBarcodeOutline tw="mx-auto text-7xl text-pink-600" />
                )}
              </motion.div>

              <h1 tw="mx-auto text-4xl font-bold mb-4 text-center text-transparent  bg-clip-text bg-gradient-to-br from-yellow-300 via-pink-500 to-indigo-600 ">
                {selectedModel === 1 ? "Analyse sentence" : "Generate Grammar"}
              </h1>
            </motion.div>
            {!loading && (
              <div tw="h-10 w-full lg:w-2/6 mx-auto my-4 font-bold text-center uppercase flex rounded-3xl border border-pink-300 shadow">
                <div tw="flex w-full">
                  <SelectableHalf
                    selected={selectedModel === 1}
                    direction="left"
                    onClick={() => setSelectedModel(1) || setResult(undefined)}
                  >
                    <motion.div
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      tw="m-auto"
                    >
                      Test Grammar
                    </motion.div>
                  </SelectableHalf>
                  <SelectableHalf
                    selected={selectedModel === 2}
                    direction="right"
                    onClick={() => setSelectedModel(2) || setResult(undefined)}
                  >
                    <motion.div
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      tw="m-auto"
                    >
                      Generate Grammar
                    </motion.div>
                  </SelectableHalf>
                </div>
              </div>
            )}
            {selectedModel === 1 ? (
              <TextInput
                placeholder="Enter a sentence to scan here"
                value={sent}
                onChange={(e) => setSent(e.target.value)}
              />
            ) : (
              <div tw="flex flex-col">
                <TextInput
                  tw="mb-4"
                  placeholder="Enter a POS-tagged Corpus here"
                  value={corpus}
                  onChange={(e) => setCorpus(e.target.value)}
                />

                <TextInput
                  placeholder="Enter test senteces here"
                  value={testCorpus}
                  onChange={(e) => setTestCorpus(e.target.value)}
                />
              </div>
            )}
            {loading ? (
              <div tw="flex flex-col h-10 m-3 mx-auto text-pink-600 ">
                <div tw="my-2">
                  <ImSpinner9 tw="animate-spin text-7xl text-center mx-auto" />
                </div>
                <div tw="mx-auto font-bold">Analyzing</div>
              </div>
            ) : (
              <Button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                style={{ outline: "none" }}
                onClick={
                  selectedModel === 1
                    ? handleAnalyzeText
                    : handleGenerateGrammar
                }
              >
                <IoSearchSharp tw="my-auto mr-2 text-lg " />
                <span tw="my-auto">
                  {selectedModel === 1
                    ? `Analyse ${result ? "new" : ""} sentence`
                    : `Generate ${result ? "new" : ""} grammar`}
                </span>
              </Button>
            )}
          </motion.div>

          {selectedModel === 1
            ? result && <AnalyzeResults result={result} type="test" />
            : result && <AnalyzeResults result={result} type="generate" />}
        </MainContent>
      </Container>
    </AnimateSharedLayout>
  );
}

export default App;
