import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class UnusedArgBlock extends React.Component {
  constructor() {
    super();
    this.state = { collapse: false };
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  render() {
    if (this.props.name == []) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Argument Usage</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Argument usage is evaluate based on how many arguments are
              declared but not used.
            </p>
            <p>There is no unused argument.</p>
          </div>
        </div>
      );
    } else if (this.props.name == ["Not evaluated"]) {
      return <div />;
    } else if (this.props.name == ["There is no argument in your project."]) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Argument Usage</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no argument in your project.</p>
          </div>
        </div>
      );
    } else {
      const columns = [
        {
          Header: "Argument ID",
          accessor: "index"
        },
        {
          Header: "Argument Name",
          accessor: "argumentName"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Argument Usage</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Argument usage is evaluate based on how many arguments are
              declared but not used. An unused argument should be deleted. Such
              arguments include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
