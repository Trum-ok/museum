import React, { useState } from "react";
import { BoxContainer, FormContainer, Input, SubmitButton } from "./common";
import { Marginer } from "../marginer";
import { authenticate } from "../../auth"; // Импортируем функцию аутентификации

export function LoginForm(props) {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault(); 
    try {
      const token = await authenticate(login, password); // Вызываем функцию аутентификации

      if (token) {
        localStorage.setItem('token', token);
        console.log(token)
        window.location.href = '/admin';
      } else {
        console.error('Authentication failed');
      }
    } catch (error) {
      console.error('An error occurred while processing the request:', error);
    }
  };

  return (
    <BoxContainer>
      <FormContainer onSubmit={handleSubmit}>
        <Input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <SubmitButton type="submit">Signin</SubmitButton>
      </FormContainer>
      <Marginer direction="vertical" margin={10} />
      <Marginer direction="vertical" margin="1.6em" />
      <Marginer direction="vertical" margin="5px" />
    </BoxContainer>
  );
}
