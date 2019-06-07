import React, { Component } from 'react';
import {Text, Linking } from 'react-native';
import {withStyles} from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import MaterialTable from 'material-table';
import AddBox from '@material-ui/icons/AddBox';
import ArrowUpward from '@material-ui/icons/ArrowUpward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';

const tableIcons = {
  Add: AddBox,
  Check: Check,
  Clear: Clear,
  Delete: DeleteOutline,
  DetailPanel: ChevronRight,
  Edit: Edit,
  Export: SaveAlt,
  Filter: FilterList,
  FirstPage: FirstPage,
  LastPage: LastPage,
  NextPage: ChevronRight,
  PreviousPage: ChevronLeft,
  ResetSearch: Clear,
  Search: Search,
  SortArrow: ArrowUpward,
  ThirdStateCheck: Remove,
  ViewColumn: ViewColumn
};

const styles = theme => ({
   root: {
      width: '100%',
      marginTop: theme.spacing(3),
      overflowX: 'auto',
   },
   table: {
      minWidth: 700,
   },
});

var rows = [];

class Demo extends Component {
   componentDidMount() {
      this.setState({ isLoading: true });
      fetch('/retrieve-doggo-data')
         .then(res => {
            if(res.ok) {
               console.log(res)
               return res.json();
            } else {
               throw new Error('Something went wrong...');
            }
         })
         .then(data => {
            console.log(data)
            this.setState({
               doggos:data,
               isLoading: false,
            })})
         .catch(error=> this.setState({ error, isLoading:false }));
   }

   render() {
      const { classes } = this.props;

      if (this.state) {
         if (this.state.isLoading) {
            return null;
         }
      } else {
         return null;
      }
      //console.log("state")
      //console.log(this.state)
      //console.log("doggos")
      //console.log(this.state.doggos)
      //console.log("json doggos")
      //console.log(JSON.parse(this.state.doggos))

      //rows = JSON.parse(this.state.doggos)
      rows = this.state.doggos
      var borderCss = '1.5px solid gray'
      //rows = this.state;
      return (
         //<div style={{ maxWidth: "100%" }}>
         <MaterialTable
         columns={[
            { title: "Dog", field: "doggo", sorting: false,
              render: rowData => <img src={'http://' + rowData.doggo} height="300" alt=""/>,
              cellStyle: {borderRight: borderCss, borderTop: borderCss, borderBottom: borderCss},
            },
            { title: "Name", field: "name", cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss} },
            { title: "Breed", field: "breed", cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss}},
            { title: "Age", field: "age",
               customSort: (a, b) => {
                  var regex = /^\d+/;
                  var aAge = regex.exec(a.age);
                  //console.log(a.age);
                  //console.log(aAge);
                  var bAge = regex.exec(b.age);
                  //console.log(b.age);
                  //console.log(bAge);
                  return aAge - bAge;
               }, cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss}
            },
            { title: "Sex", field: "sexSN", cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss}},
            { title: "Intake Date", field: "intake", cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss, width: 75}
            },
            { title: "Dog Link", field: "dogLink", sorting: false,
              render: rowData => <Text style={styles.TextStyle} onPress={ ()=> Linking.openURL(rowData.dogLink) } > Dog Page Link </Text>,
               cellStyle: {border: borderCss, borderTop: borderCss, borderBottom: borderCss},
            },
            { title: "Shelter", field: "shelter", cellStyle: {borderLeft: borderCss, borderTop: borderCss, borderBottom: borderCss}}
         ]}
         data={rows}
         option={{
            sorting: true
         }}
         options={{
            headerStyle: {
               backgroundColor: '#01579b',
               color: '#FFF'
            }
         }}
         icons={tableIcons}
         title="Roseville Dog Adoption Search"
         style={{ width: '95%', marginLeft: '2.5%'}}
         className={classes.root}
         />
         //</div>
      );
   }
}

Demo.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Demo);
