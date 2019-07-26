import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class NoLMExpBlock extends React.Component {
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
          <h3 onClick={this.toggle.bind(this)}>Try Catch Logging</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Try catch logging is evaluated by checking if all exceptions are
              handled by log messages.
            </p>
            <p>There is no exception that is not handled by log message.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["There is no catch in your project."]) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Try Catch Logging</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no catch in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["Not evaluated"]) {
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
          <h3 onClick={this.toggle.bind(this)}>Try Catch Logging</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Try catch logging is evaluated by checking if all exceptions are
              handled by log messages. An exception should always be logged.
              Exceptions that are not logged include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
