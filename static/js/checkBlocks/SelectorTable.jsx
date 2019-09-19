import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
<link
  rel="stylesheet"
  href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
></link>;

export default class SelectorTable extends React.Component {
  render() {
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
        Header: "File",
        accessor: "filePath"
      },
      {
        Header: "Project",
        accessor: "projectId"
      }
    ];
    return (
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
        showPageSizeOptions={false}
      />
    );
  }
}
