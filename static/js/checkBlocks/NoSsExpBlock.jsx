import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class NoSsExpBlock extends React.Component {
  constructor() {
    super();
    this.state = { collapse: false };
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  render() {
    if (this.props.name.data == []) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Try Catch Screenshot</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Try catch screenshot is evaluated by checking if all exceptions
              are handled by screenshot.
            </p>
            <p>There is no exception that is not handled by screenshot.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["There is no catch in your project."]) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Try Catch Screenshot</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no catch in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == ["Not evaluated"]) {
      return <div />;
    } else {
      const columns = [
        {
          Header: "TryCatch ID",
          accessor: "index"
        },
        {
          Header: "Catch",
          accessor: "Catch Id"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Try Catch Screenshot</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Try catch screenshot is evaluated by checking if all exceptions
              are handled by screenshot. An exception should always be recorded
              by a screenshot activity. Exceptions that are not handled by
              screenshot include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
