import React, { Component } from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import { Container, Menu, Button, Icon } from 'semantic-ui-react';
import LoginProvider from './user/login-provider';
import BudgetsPovider from './budget/budgets-provider';

class App extends Component {
    state = {
        loggedIn: undefined,
        username: undefined,
        email: undefined,
        pass: undefined
    };

    constructor(props) {
        super(props);

        this.logOut = this.logOut.bind(this);
    }

    logOut() {
        console.log('Logging out');
        fetch('/api/auth/logout')
            .then(response => response.blob())
            .then(body => {
                console.log(body);
                this.setState({ loggedIn: false, username: undefined, pass: undefined });
            })
            .catch(err => {
                console.error(err);
            });
    }

    render() {
        const { loggedIn } = this.state;
        const logOutButton = (
            <Button inverted color="red" icon labelPosition="right" onClick={this.logOut}>
                Log Out
                <Icon name="sign out" />
            </Button>
        );
        return (
            <div>
                <Menu fixed="top" inverted>
                    <Menu.Menu />
                    <Menu.Menu position="right">
                        {this.state.loggedIn && <Menu.Item>{logOutButton}</Menu.Item>}
                    </Menu.Menu>
                </Menu>

                <Container style={{ marginTop: '5em', marginBottom: '5em' }}>
                    {loggedIn ? (
                        <div>
                            <h1>Hello {this.state.username}</h1>
                            <BudgetsPovider />
                        </div>
                    ) : (
                        <LoginProvider
                            onLoggedIn={userInfo => {
                                console.log('Logged In: ', userInfo);
                                this.setState({
                                    loggedIn: true,
                                    username: userInfo.username
                                });
                            }}
                            onLoggedOut={() => {
                                console.log('Logged out...');
                                this.setState({ loggedIn: false });
                            }}
                        />
                    )}
                </Container>
            </div>
        );
    }
}

export default App;
