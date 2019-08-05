import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class SelectorEvalBlock extends React.Component {
  constructor(props) {
    super(props);
    this.state = { collapse: false, byProject: false };
    console.log(this.props.name);
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }

  render() {
    if (this.props.name.data == ["There is no selectors in your project."]) {
      return (
        <div className="Selectors">
          <h3 onClick={this.toggle.bind(this)}>Selectors</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no no selectors in your project.</p>;
          </div>
        </div>
      );
    } else {
      const columns = [
        {
          Header: "Selector ID",
          accessor: "index",
          id: "index",
          show: false
        },
        {
          Header: "Selector",
          accessor: "selectorStr"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="Selectors">
          <h3 onClick={this.toggle.bind(this)}>Selectors</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <ReactTable
              columns={columns}
              data={this.props.name.data}
              filterable
              defaultFilterMethod={(filter, row) =>
                String(row[filter.id])
                  .toLowerCase()
                  .includes(filter.value.toLowerCase())
              }
              defaultPageSize={10}
            />
          </div>
        </div>
      );
    }
  }
}
