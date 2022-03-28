import React, { useState } from 'react';

import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Collapse from "react-bootstrap/Collapse";
import Container from "react-bootstrap/Container";

function Result(props) {
    const [open, setOpen] = useState(false);
    return (
        <Card>
            <Card.Body>
                <Card.Title>{props.title}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">Authors</Card.Subtitle>
                <Card.Text>
                    Paper Abstract
                </Card.Text>
                <Button
                    onClick={() => setOpen(!open)}
                    aria-controls="example-collapse-text"
                    aria-expanded={open}
                >
                    Referenced by
                </Button>
                <Button variant="primary">References</Button>
                <Collapse in={open}>
                    <div id="example-collapse-text">
                        <Container>
                            <Card.Link href="#">Card Link</Card.Link>
                            <Card.Link href="#">Card Link</Card.Link>
                            <Card.Link href="#">Card Link</Card.Link>
                        </Container>
                    </div>
                </Collapse>
            </Card.Body>
        </Card >
    )
}

export default Result