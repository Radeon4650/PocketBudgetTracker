import React, { Component } from 'react';
import LoginForm from './login-form';

class LoginProvider extends Component {
    state = {
        loggedIn: undefined,
        username: undefined,
        email: undefined,
        pass: undefined
    };

    constructor(props) {
        super(props);

        this.onLoggedIn = props.onLoggedIn;
        this.onLoggedOut = props.onLoggedOut;

        this.logIn = this.logIn.bind(this);
        this.createUser = this.createUser.bind(this);
        this.getCurrentUser = this.getCurrentUser.bind(this);
    }

    componentDidMount() {
        this.getCurrentUser();
    }

    getCurrentUser() {
        fetch('/api/auth/login', { redirect: 'error' })
            .then(response => response.json())
            .then(body => {
                console.log(body);
                this.setState(
                    {
                        loggedIn: true,
                        email: body.username
                    },
                    () => this.onLoggedIn(body)
                );
            })
            .catch(err => {
                console.log(err);
                this.setState({ loggedIn: false }, () => this.onLoggedOut());
            });
    }

    logIn() {
        const data = {
            login: this.state.email,
            password: this.state.pass
        };
        const options = {
            method: 'post',
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            redirect: 'error',
            body: JSON.stringify(data)
        };
        fetch('/api/auth/login', options)
            .then(response => response.blob())
            .then(body => {
                console.log(body);
                this.getCurrentUser();
            })
            .catch(err => {
                console.error(err);
                this.getCurrentUser();
            });
    }

    createUser() {
        const data = {
            username: this.state.username,
            email: this.state.email,
            password: this.state.pass
        };
        const options = {
            method: 'post',
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            body: JSON.stringify(data)
        };
        fetch('/api/auth/create', options)
            .then(response => response.blob())
            .then(body => {
                console.log(body);
                this.logIn();
            })
            .catch(err => {
                console.error(err);
                this.setState({ loggedIn: false });
            });
    }

    render() {
        return (
            <LoginForm
                onLoginClick={this.logIn}
                onUserCreateClick={this.createUser}
                onUserNameChange={(e, { name, value }) => this.setState({ [name]: value })}
                onEmailChange={(e, { name, value }) => this.setState({ [name]: value })}
                onPasswordChange={(e, { name, value }) => this.setState({ [name]: value })}
            />
        );
    }
}

export default LoginProvider;
