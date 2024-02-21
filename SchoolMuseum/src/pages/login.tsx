import styled from "styled-components";
import AccountBox from "../components/accountBox/index"

const AppContainer = styled.div`
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

function Login() {
  return (
    <>
    <AppContainer>
        <AccountBox />
    </AppContainer>
    </>
  )
}

export default Login