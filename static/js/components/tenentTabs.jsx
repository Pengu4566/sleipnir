import React from "react";
import classnames from "classnames";
// import Col from "react-bootstrap/Col";
// import Row from "react-bootstrap/Row";
// import Tab from "react-bootstrap/Tab";
// import Nav from "react-bootstrap/Nav";
import { Col, Row, Tab, Nav, Form, Button } from "react-bootstrap";
import styles from "./../../scss/components/tenant_tabs.scss";

export default class TenantTabs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      newTenantName: "",
      oldTenantName: ""
    };
    this.editTenant = this.editTenant.bind(this);
    this.onEditInput = this.onEditInput.bind(this);
  }

  resetState(e) {
    this.setState({ newTenantName: "", oldTenantName: "" });
  }

  editTenant(e, mode) {
    e.preventDefault();
    switch (mode) {
      case "create":
        console.log("create tenant");
        break;
      case "edit":
        console.log("edit tenant");

        break;
      case "delete":
        console.log("delete tenant");

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
      <Tab.Container id="tenentTabs" defaultActiveKey="createTenant">
        <Row>
          <Col sm={3}>
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link
                  eventKey="createTenant"
                  onClick={e => this.resetState(e)}
                >
                  Create Tenant
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="editTenant"
                  onClick={e => this.resetState(e)}
                >
                  Edit Tenant
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="deleteTenant"
                  onClick={e => this.resetState(e)}
                >
                  Delete Tenant
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            <Tab.Content>
              <Tab.Pane eventKey="createTenant">
                <Form onSubmit={e => this.editTenant(e, "create")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Tenant Name
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newTenantName"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Tenant Name"
                      />
                    </Col>
                  </Form.Group>

                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Create Tenant</Button>
                    </Col>
                  </Form.Group>
                </Form>
              </Tab.Pane>
              <Tab.Pane eventKey="editTenant">
                <Form onSubmit={e => this.editTenant(e, "edit")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Tenant
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="oldTenantName"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Old Tenant Name"
                      />
                    </Col>
                  </Form.Group>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      New Name
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="newTenantName"
                        onChange={e => this.onEditInput(e)}
                        placeholder="New Tenant Name"
                      />
                    </Col>
                  </Form.Group>

                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Change Tenant Setting</Button>
                    </Col>
                  </Form.Group>
                </Form>
              </Tab.Pane>
              <Tab.Pane eventKey="deleteTenant">
                <Form onSubmit={e => this.editTenant(e, "delete")}>
                  <Form.Group as={Row}>
                    <Form.Label column sm={3}>
                      Tenant Name
                    </Form.Label>
                    <Col sm={8}>
                      <Form.Control
                        name="oldTenantName"
                        onChange={e => this.onEditInput(e)}
                        placeholder="Tenant Name"
                      />
                    </Col>
                  </Form.Group>

                  <Form.Group as={Row}>
                    <Col sm={{ span: 10, offset: 3 }}>
                      <Button type="submit">Delete Tenant</Button>
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
