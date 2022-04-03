import React from "react";

import Pagination from "react-bootstrap/Pagination";

export default function PaginationElement(props) {
    let pageArray = []
    if (props.currentPage < 3) {
        pageArray = [1, 2, 3, 4, 5]
    }
    else if (props.lastPage - props.currentPage < 2) {
        pageArray = [props.lastPage - 4, props.lastPage - 3, props.lastPage - 2, props.lastPage - 1, props.lastPage]
    }
    else {
        pageArray = [props.currentPage - 2, props.currentPage - 1, props.currentPage, props.currentPage + 1, props.currentPage + 2]
    }

    let pageItemArray = pageArray.map((pageNumber) =>
        <Pagination.Item onClick={(event) => props.changePage(parseInt(event.target.text))} active={pageNumber == props.currentPage}>
            {pageNumber}
        </Pagination.Item>)

    return (
        <Pagination>
            <Pagination.First onClick={(event) => props.changePage(1)} />
            <Pagination.Prev onClick={(event) => props.changePage(props.currentPage - 1)} />
            {pageItemArray}
            <Pagination.Next onClick={(event) => props.changePage(props.currentPage + 1)} />
            <Pagination.Last onClick={(event) => props.changePage(props.lastPage)} />
        </Pagination>
    )
}