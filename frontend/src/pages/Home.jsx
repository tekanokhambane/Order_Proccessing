import React from 'react'
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { Container, Button } from 'react-bootstrap';
import axios from 'axios';
import PropTypes from 'prop-types';


const Home = ({ addToCart }) => {
    const [products, setProducts] = React.useState([]);
    React.useEffect(() => {
        axios
            .get("/api/products")
            .then((res) => {
                console.log(res.data);
                setProducts(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);


    return (

        <Container className='pt-5'>
            <Row xs={1} md={4} className="g-4">
                {products.map((product, idx) => (
                    <Col key={idx}>
                        <Card>
                            <Card.Img variant="top" style={{ height: "200px" }} src={product.image} />
                            <Card.Body>
                                <Card.Title>{product.name}</Card.Title>
                                <Card.Text>
                                    {product.description}
                                </Card.Text>
                            </Card.Body>
                            <Card.Footer className='d-flex justify-content-between align-items-center'>
                                <small className="text-muted">${product.price}</small>
                                <Button variant="primary" onClick={() => addToCart(product)} >
                                    Add to cart
                                </Button>
                            </Card.Footer>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>

    );
}

Home.propTypes = {
    addToCart: PropTypes.func
};


export default Home