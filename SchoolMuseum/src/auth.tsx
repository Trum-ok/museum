    import * as JWT  from 'jose';

    export function authenticate(login: string, password: string) {
        // запрос к api
        // и получение токена в случае успешной авторизации
        return fetch('http://localhost:8080/api/auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login, password }),
        })
        .then(response => response.json())
        .then(data => {
            const { token } = data;
            localStorage.setItem('token', token);
            return token;
        });
    }

    export async function isAuthenticated() {
        // проверка аутентификации юзера при попытке перехода на /admin/*
        const token = localStorage.getItem('token');

        if (!token) {
            return false;
        }

        const secret = new TextEncoder().encode(
            "_Yr019xMxv6ZM1TGTWMbgRK-W3RjdMYpdq_g9yHUw8jGWDlpc85gvm0ExXPNqNnVKNoQcB6OvIcPKCBtVrClsw",
        );

        try {
            const result = await JWT.jwtVerify(token, secret);
            console.log('Token verification result:', result);
            return true;
        } catch (error) {
            console.error('An error occurred while verifying the token:', error);
            return false;
        }
    }
