import React from "react";

import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';
import Stack from 'react-bootstrap/Stack';
import Spinner from 'react-bootstrap/Spinner';

import Result from "./result";

class Search extends React.Component {
    constructor(props) {
        super(props);
        this.handleSearch = this.handleSearch.bind(this)
        this.state = {
            searchBarInput: "",
            displayLoading: false,
            searchResults: []
        }
    }

    async requestSearchResults(keywords) {
        let url = "https://api.crossref.org/works?query=";
        let encoded_query = encodeURIComponent(keywords.join(" "));
        let response = await fetch(url + encoded_query, { method: "GET" });
        let res_obj = await response.json();
        return res_obj
    }

    async handleSearch() {
        this.setState({
            displayLoading: true,
            searchResults: []
        })

        let resp = await this.requestSearchResults(this.state.searchBarInput.split(" "));
        this.setState({
            displayLoading: false,
            searchResults: resp.message.items,
        })

        // alert(JSON.stringify(results))
    }

    render() {
        const titles = this.state.searchResults.map((item) => item.title[0])
        return (
            <Container>
                <Stack gap={3}>
                    <div className="container gy-3">
                        <InputGroup className="mb-3">
                            <FormControl aria-describedby="basic-addon2" onChange={e => this.setState({ searchBarInput: e.target.value })} />
                            <Button variant="primary" id="button-addon2" onClick={this.handleSearch}>
                                Search
                            </Button>
                        </InputGroup>

                        {
                            this.state.displayLoading &&
                            <Spinner animation="border" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>
                        }
                    </div>
                    {titles.map((title) => <Result title={title} />)}
                </Stack>
            </Container>
        );
    }
}

export default Search;