import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';

function BudgetPage(budgets) {
    return (
        <div>
            {!budgets.budgets.categories ? (
                <pre>You have no entries in your budget</pre>
            ) : (
                budgets.budgets.categories.map(category => (
                    <Table key={category.id} celled>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell textAlign="center" colSpan="4">
                                    {category.name}
                                </Table.HeaderCell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>Number</Table.HeaderCell>
                                <Table.HeaderCell>Date</Table.HeaderCell>
                                <Table.HeaderCell>Title</Table.HeaderCell>
                                <Table.HeaderCell>Amount</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {category.items.map(item => (
                                <Table.Row key={item.id}>
                                    <Table.Cell>{item.id}</Table.Cell>
                                    <Table.Cell>{item.date}</Table.Cell>
                                    <Table.Cell>{item.title}</Table.Cell>
                                    <Table.Cell>{`${item.amount}  ${item.currency}`}</Table.Cell>
                                </Table.Row>
                            ))}
                        </Table.Body>
                    </Table>
                ))
            )}
        </div>
    );
}

export default BudgetPage;
