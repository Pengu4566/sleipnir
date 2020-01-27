import React from "react";
import classnames from "classnames";
import { Col, Row, Tab, Nav, Form, Button } from "react-bootstrap";
import styles from "./../../scss/components/user_tabs.scss";

export default class UserTabs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tenant: "",
      newUsername: "",
      oldUsername: "",
      newUserEmail: "",
      oldUserEmail: "",
      newUserPassword: "",
      oldUserPassword: ""
    };
    this.editUser = this.editUser.bind(this);
    this.onEditInput = this.onEditInput.bind(this);
  }

  resetState(e) {
    this.setState({
      tenant: "",
      newUsername: "",
      oldUsername: "",
      newUserEmail: "",
      oldUserEmail: "",
      newUserPassword: "",
      oldUserPassword: ""
    });
  }

  editUser(e, mode) {
    e.preventDefault();
    switch (mode) {
      case "create":
        console.log("create user");
        break;
      case "edit":
        console.log("edit user");

        break;
      case "delete":
        console.log("delete user");

        break;
    }
  }

  onEditInput(e) {
    let name = e.target.name;
    this.setState({ [name]: e.target.value }, () => {
      console.log(this.state);
    });
  }

  render() {
    return (
      <Tab.Container id="userTabs" defaultActiveKey="createUser">
        <Row>
          <Col sm={3}>
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link
                  eventKey="createUser"
                  onClick={e => this.resetState(e)}
                >
                  Create User
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="editUser" onClick={e => this.resetState(e)}>
                  Edit User
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="deleteUser"
                  onClick={e => this.resetState(e)}
                >
                  Delete User
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            <Tab.Content>
              <Tab.Pane eventKey="createUser">
                <Form onSubmit={e => this.editUser(e, "create")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Username
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUsername"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Username"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      User Email
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUserEmail"
                        onChange={e => this.onEditInput(e)}
                        placeholder="User Email"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      User Password
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUserPassword"
                        type="password"
                        onChange={e => this.onEditInput(e)}
                        placeholder="User Password"
                      />
                    </Col>
                  </Form.Group>

                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Create User</Button>
                    </Col>
                  </Form.Group>
                </Form>
              </Tab.Pane>
              <Tab.Pane eventKey="editUser">
                <Form onSubmit={e => this.editUser(e, "edit")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Username
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="oldUsername"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Username"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      New Username
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUsername"
                        onChange={e => this.onEditInput(e)}
                        placeholder="New Username"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      User Email
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUserEmail"
                        onChange={e => this.onEditInput(e)}
                        placeholder="User Email"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      User Password
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newUserPassword"
                        type="password"
                        onChange={e => this.onEditInput(e)}
                        placeholder="User Password"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Change User Setting</Button>
                    </Col>
                  </Form.Group>
                </Form>
              </Tab.Pane>
              <Tab.Pane eventKey="deleteUser">
                <Form onSubmit={e => this.editUser(e, "delete")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Username
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="oldUsername"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Username"
                      />
                    </Col>
                  </Form.Group>

                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Delete User</Button>
                    </Col>
                  </Form.Group>
                </Form>
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
    );
  }
}
