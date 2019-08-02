import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class ImproperNamedVarBlock extends React.Component {
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
          <h3 onClick={this.toggle.bind(this)}>Variable Naming</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Variable naming is evaluated according to camel case rule and the
              variable's data type.
            </p>
            <p>
              According to our best practice, there is no improperly named
              variable.
            </p>
          </div>
        </div>
      );
    } else if (
      this.props.name.data == ["There is no variable in your project."]
    ) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>Variable Naming</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no variable in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["Not evaluated"]) {
      return <div />;
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
          <h3 onClick={this.toggle.bind(this)}>Variable Naming</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Variable naming is evaluated according to camel case rule and the
              variable's data type. Variables that are not properly named
              include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
