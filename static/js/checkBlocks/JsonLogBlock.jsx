import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class JsonLogBlock extends React.Component {
  constructor() {
    super();
    this.state = { collapse: false };
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  render() {
    const columns = [
      {
        Header: "Project ID",
        accessor: "index"
      },
      {
        Header: "Project Name",
        accessor: "projectDetail.projectName"
      },
      {
        Header: "Project Description",
        accessor: "projectDetail.projectDescription"
      },
      {
        Header: "Template",
        accessor: "templateComment"
      }
    ];
    if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Project.Json Logging</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              The project.json file should contain your own project name and
              description. Default values are not recommended.
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
