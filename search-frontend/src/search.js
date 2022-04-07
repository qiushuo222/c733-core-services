import React from "react";

import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';
import Stack from 'react-bootstrap/Stack';
import Spinner from 'react-bootstrap/Spinner';

import Result from "./result";
import PaginationElement from "./pagination";

class Search extends React.Component {
    constructor(props) {
        super(props);
        this.handleSearch = this.handleSearch.bind(this)
        this.changePage = this.changePage.bind(this)
        this.state = {
            searchBarInput: "",
            displayLoading: false,

            resultPerPage: 0,
            totalResults: 0,

            currentPage: 1,
            lastPage: 0,

            searchResults: [],
        }
    }

    async requestSearchResults(keywords, startIndex) {
        let url = "/api/search?keywords=";
        let encoded_query = encodeURIComponent(`"${keywords.join(" ")}"`);
        let response = await fetch(`${url}${encoded_query}&start=${startIndex}`, { method: "GET" });
        let res_obj = await response.json();
        return res_obj
    }

    async handleSearch() {
        this.setState({
            displayLoading: true,
            searchResults: []
        })
        
        let startIndex = (this.state.currentPage - 1) * this.state.resultPerPage
        let resp = await this.requestSearchResults(this.state.searchBarInput.split(" "), startIndex.toString());

        this.setState({
            displayLoading: false,
            searchResults: resp.results,
            totalResults: resp.totalResults,

            currentPage: Math.floor(resp.startIndex / resp.itemsPerPage) + 1,
            lastPage: Math.floor(resp.totalResults / resp.itemsPerPage),
            resultPerPage: resp.itemsPerPage
        })

    }

    changePage(targetPage) {
        this.setState({
            currentPage: targetPage
        }, () => {
            this.handleSearch()
        })
    }

    render() {
        this.state.searchResults.sort((a, b) => { return b.score - a.score })
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
                    {
                        this.state.searchResults.map((item) => <Result key={item.paper_page} title={item.title} authors={item.authors} score={item.score} abstract={item.abstract} paperLink={item.paper_page} pdfLink={item.pdf_link} />)
                    }
                </Stack>
                {   this.state.searchResults.length !== 0 &&
                    <PaginationElement totalLen={5} currentPage={this.state.currentPage} lastPage={this.state.lastPage} changePage={this.changePage} />
                }
            </Container>
        );
    }
}

export default Search;