import tw from "twin.macro";

const Container = tw.div`container flex h-full p-4`;
const SideBarContainer = tw.div`w-80 m-4`;
const SideBar = tw.div`m-3 p-4 w-full h-full rounded-3xl bg-gray-200`;
const MainContent = tw.div`w-full`;

function App() {
  return (
    <Container>
      <MainContent>helo</MainContent>

      <SideBarContainer>
        <SideBar>Hello</SideBar>
      </SideBarContainer>
    </Container>
  );
}

export default App;
