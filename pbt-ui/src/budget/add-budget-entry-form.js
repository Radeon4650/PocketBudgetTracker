import React, { Component } from 'react';
import { Table, Button, Header, Icon, Segment, Grid, Divider, Form } from 'semantic-ui-react';

function AddBudgetEntryForm({ onValueChange, onSubmit }) {
    return (
        <Segment color="olive">
            <h3>Add entry</h3>
            <Form size="mini" onSubmit={onSubmit}>
                <Form.Group inline>
                    <Form.Field>
                        <Form.Input name="category" placeholder="Enter category" onChange={onValueChange} />
                    </Form.Field>
                    <Form.Field>
                        <Form.Input name="title" placeholder="Enter title" onChange={onValueChange} />
                    </Form.Field>
                    <Form.Field>
                        <Form.Input name="amount" placeholder="Enter amount" onChange={onValueChange} />
                    </Form.Field>
                    <Form.Field>
                        <Form.Button type="submit">Submit</Form.Button>
                    </Form.Field>
                </Form.Group>
            </Form>
        </Segment>
    );
}

export default AddBudgetEntryForm;
