import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class JsonLogBlock extends React.Component {
  render() {
    const columns = [
      {
        Header: "Project ID",
        accessor: "index",
        id: "index"
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

    let pgSize = this.props.name.data.length;

    return (
      <ReactTable
        columns={columns}
        data={this.props.name.data}
        defaultPageSize={pgSize}
        showPageSizeOptions={false}
        showPagination={false}
      />
    );
  }
}
