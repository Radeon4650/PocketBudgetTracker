import React, { Component } from 'react';
import BudgetPage from './budget-page';
import AddBudgetEntryForm from './add-budget-entry-form';

class BudgetsPovider extends Component {
    state = {
        category: undefined,
        date: undefined,
        title: undefined,
        amount: undefined,
        currency: 'UAH',
        budgets: []
    };

    componentDidMount() {
        this.getBudgets();
        this.addEntry = this.addEntry.bind(this);
        this.valueChange = this.valueChange.bind(this);
    }

    getBudgets() {
        fetch('/api/budget')
            .then(res => res.json())
            .then(data => {
                console.log(data);
                this.setState({ budgets: data });
            })
            .catch(err => {
                console.log(err);
            });
    }

    addEntry() {
        console.log(this.state);
        const data = {
            category: this.state.category,
            date: new Date().toISOString(),
            title: this.state.title,
            amount: this.state.amount,
            currency: this.state.currency
        };
        const options = {
            method: 'post',
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            body: JSON.stringify(data)
        };
        fetch('/api/budget', options)
            .then(response => response.blob())
            .then(body => {
                console.log(body);
                this.getBudgets();
            })
            .catch(err => {
                console.error(err);
            });
    }

    valueChange(e, { name, value }) {
        this.setState({ [name]: value });
    }

    render() {
        return (
            <div>
                <AddBudgetEntryForm onValueChange={this.valueChange} onSubmit={this.addEntry} />
                <BudgetPage budgets={this.state.budgets} />
            </div>
        );
    }
}

export default BudgetsPovider;
