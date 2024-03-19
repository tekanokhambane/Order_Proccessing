import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { NavDropdown, Button } from 'react-bootstrap';
import { BsCart } from 'react-icons/bs';
import Badge from 'react-bootstrap/Badge';
import PropTypes from 'prop-types';


function NavbarItem({ cartItems, toggleDrawer }) {
    return (
        <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand href="/">BsShop</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="#features">Features</Nav.Link>
                        <Nav.Link href="#pricing">Pricing</Nav.Link>
                        <NavDropdown title="Dropdown" id="collapsible-nav-dropdown">
                            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">
                                Another action
                            </NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item href="#action/3.4">
                                Separated link
                            </NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Nav>
                        <Nav.Link href="/login">Login</Nav.Link>

                        <Button variant="" onClick={toggleDrawer} className='position-relative'>
                            <BsCart /> <Badge bg="info" pill className='position-absolute'>{cartItems.length}</Badge>
                            <span className="visually-hidden">items in cart</span>
                        </Button>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
    //k2024028996



}


NavbarItem.propTypes = {
    cartItems: PropTypes.array
}


export default NavbarItem;