import React from 'react';
import Card from "react-bootstrap/Card";

function Result(props) {
    return (
        <Card>
            <Card.Body>
                <Card.Title>
                    <a href={props.paperLink} target="_blank" rel="noreferrer">{props.title}</a>
                    <a href={props.pdfLink} target="_blank" rel="noreferrer"> [PDF]</a>
                </Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{props.authors.join(", ")}</Card.Subtitle>
                <Card.Text>
                    {props.abstract}
                </Card.Text>
            </Card.Body>
        </Card >
    )
}

export default Result;