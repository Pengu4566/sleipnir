import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class ArginAnnotBlock extends React.Component {
  constructor() {
    super();
    this.state = { collapse: false };
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  render() {
    if (this.props.name.data == ["There is no argument in this project."]) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>
            Argument Explanation in Annotation
          </h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow.
            </p>
            <p>There is no argument in this project.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == []) {
      return (
        <div className="single_check">
          <h3 onClick={this.toggle.bind(this)}>
            Argument Explanation in Annotation
          </h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow.
            </p>
            <p>
              There is no arguments that are not mentioned in the annotation.
            </p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["Not evaluated"]) {
      return <div />;
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
          <h3 onClick={this.toggle.bind(this)}>
            Argument Explanation in Annotation
          </h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow. Arguments that are not even mentioned in the annotation
              include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
