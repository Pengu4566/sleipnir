import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class UnusedVarBlock extends React.Component {
  render() {
    if (this.props.name == []) {
      return (
        <div className="single_check">
          <h3>Variable Usage</h3>
          <div className="check_explain">
            <p>
              Variable usage is evaluate based on how many variables are
              declared but not used.
            </p>
            <p>There is no unused variable.</p>
          </div>
        </div>
      );
    } else if (this.props.name == ["Not evaluated"]) {
      return <div />;
    } else if (this.props.name == ["There is no variable in your project."]) {
      return (
        <div className="single_check">
          <h3>Variable Usage</h3>
          <div className="check_explain">
            <p>There is no variable in your project.</p>
          </div>
        </div>
      );
    } else {
      const columns = [
        {
          Header: "Variable ID",
          accessor: "index"
        },
        {
          Header: "Variable Name",
          accessor: "variableName"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="single_check">
          <h3>Variable Usage</h3>
          <div className="check_explain">
            <p>
              Variable usage is evaluate based on how many variables are
              declared but not used. An unused variable should be deleted. Such
              variables include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
