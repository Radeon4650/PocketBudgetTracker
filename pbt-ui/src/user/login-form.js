import React from 'react';
import { Button, Header, Icon, Segment, Grid, Divider, Form } from 'semantic-ui-react';

function LoginForm({ onLoginClick, onUserCreateClick, onUserNameChange, onEmailChange, onPasswordChange }) {
    return (
        //         loginForm() {
        //     if (this.state.loggedIn === undefined) {
        //         return <h5>Loading...</h5>;
        //     }

        //     return (

        //     );
        // }
        <Segment placeholder>
            <Grid columns={2} stackable textAlign="center">
                <Divider vertical>Or</Divider>

                <Grid.Row verticalAlign="middle">
                    <Grid.Column>
                        <Header icon>
                            <Icon name="sign in" />
                            Log In
                        </Header>
                        <Form onSubmit={onLoginClick}>
                            <Form.Field>
                                <label>User Email</label>
                                <Form.Input name="email" placeholder="User Email" onChange={onUserNameChange} />
                            </Form.Field>
                            <Form.Field>
                                <label>Password</label>
                                <Form.Input name="pass" placeholder="Password" onChange={onPasswordChange} />
                            </Form.Field>
                            <Button type="submit">Log in</Button>
                        </Form>
                    </Grid.Column>

                    <Grid.Column>
                        <Header icon>
                            <Icon name="user" />
                            Create a new user
                        </Header>
                        <Form onSubmit={onUserCreateClick}>
                            <Form.Field>
                                <label>User Name</label>
                                <Form.Input name="username" placeholder="User Name" onChange={onUserNameChange} />
                            </Form.Field>
                            <Form.Field>
                                <label>Email</label>
                                <Form.Input name="email" placeholder="User Email" onChange={onEmailChange} />
                            </Form.Field>
                            <Form.Field>
                                <label>Password</label>
                                <Form.Input name="pass" placeholder="Password" onChange={onPasswordChange} />
                            </Form.Field>
                            <Button type="submit">Create</Button>
                        </Form>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        </Segment>
    );
}

export default LoginForm;
