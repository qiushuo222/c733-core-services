import React from "react";

import Pagination from "react-bootstrap/Pagination";

export default function PaginationElement(props) {
    let startAt = Math.max(1, props.currentPage - Math.floor(props.totalLen / 2))
    let lowerHalfLen = props.totalLen - (props.currentPage - startAt)
    let endAt = Math.min(props.currentPage + lowerHalfLen, props.lastPage)

    let pageArray = [...Array(endAt - startAt).keys()].map(i => i + startAt)

    let pageItemArray = pageArray.map((pageNumber) =>
        <Pagination.Item onClick={(event) => props.changePage(parseInt(event.target.text))} active={pageNumber === props.currentPage}>
            {pageNumber}
        </Pagination.Item>)

    if (startAt > 1) {
        pageItemArray.unshift(<Pagination.Ellipsis />)
        pageItemArray.unshift(<Pagination.Item onClick={(event) => props.changePage(1)}>{1}</Pagination.Item>)
    }

    if (endAt < props.lastPage) {
        pageItemArray.push(<Pagination.Ellipsis />)
        pageItemArray.push(<Pagination.Item onClick={(event) => props.changePage(props.lastPage)}>{props.lastPage}</Pagination.Item>)
    }

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