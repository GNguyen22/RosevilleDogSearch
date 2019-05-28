import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { StyleSheet, Text, View, Linking } from 'react-native';

const styles = theme => ({
   root: {
      width: '100%',
      marginTop: theme.spacing.unit * 3,
      overflowX: 'auto',
   },
   table: {
      minWidth: 700,
   },
});

let id = 0;
function createData(dog_picture, name, breed, intake_date) {
   id += 1;
   return { id, dog_picture, name, breed, intake_date};
}


const rows = [
];


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
            console.log('here');
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
      if (this.state) {
         if (this.state.isLoading) {
            return null;
         }
      } else {
         return null;
      }
      console.log("state")
      console.log(this.state)
      console.log("doggos")
      console.log(this.state.doggos)
      //console.log("json doggos")
      //console.log(JSON.parse(this.state.doggos))

      //rows = JSON.parse(this.state.doggos)
      rows = this.state.doggos

      const { classes } = this.props;
      return (
         <Paper className={classes.root}>
         <Table className={classes.table}>
         <TableHead>
         <TableRow>
         <TableCell>Doggo</TableCell>
         <TableCell align="right">Name</TableCell>
         <TableCell align="right">Breed</TableCell>
         <TableCell align="right">Age</TableCell>
         <TableCell align="right">Sex</TableCell>
         <TableCell align="right">Intake Date</TableCell>
         <TableCell align="right">Dog Link</TableCell>
         </TableRow>
         </TableHead>
         <TableBody>
         {rows.map(row => (
            <TableRow key={row.id}>
            <TableCell component="th" scope="row">
            <img src={'http://' + row.doggo} />
            </TableCell>
            <TableCell align="right">{row.name}</TableCell>
            <TableCell align="right">{row.breed}</TableCell>
            <TableCell align="right">{row.age}</TableCell>
            <TableCell align="right">{row.sexSN}</TableCell>
            <TableCell align="right">{row.intake}</TableCell>
            <TableCell align="right">
               <Text style={styles.TextStyle} onPress={ ()=> Linking.openURL(row.dogLink) } > Dog Page Link </Text>
            </TableCell>
            </TableRow>
         ))}
         </TableBody>
         </Table>
         </Paper>
      );
   }
}


function SimpleTable(props) {
   const { classes } = props;

   return (
      <Paper className={classes.root}>
      <Table className={classes.table}>
      <TableHead>
      <TableRow>
      <TableCell>Doggo</TableCell>
      <TableCell align="right">Name</TableCell>
      <TableCell align="right">Breed</TableCell>
      <TableCell align="right">Intake Date</TableCell>
      </TableRow>
      </TableHead>
      <TableBody>
      {rows.map(row => (
         <TableRow key={row.id}>
         <TableCell component="th" scope="row">
         {row.dog_picture}
         </TableCell>
         <TableCell align="right">{row.name}</TableCell>
         <TableCell align="right">{row.breed}</TableCell>
         <TableCell align="right">{row.intake}</TableCell>
         </TableRow>
      ))}
      </TableBody>
      </Table>
      </Paper>
   );
}

export default withStyles(styles)(Demo);

