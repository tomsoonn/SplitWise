import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import Files from 'react-files'

// @material-ui/icons

// core components
import Header from "components/Header/Header.jsx";
import Button from "components/CustomButtons/Button.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import homePageStyle from "assets/jss/material-kit-react/views/homePage.jsx";
import CustomInput from "../../components/CustomInput/CustomInput";

// Sections for this page

const dashboardRoutes = [];

class HomePage extends React.Component {

    constructor() {
        super();
        this.state = {
            title: '',
            email: '',
            participants: [],
            bill: {},
            due: ''
        };
        this.uploadReceipt = this.uploadReceipt.bind(this);
        this.onFileChange = this.onFileChange.bind(this);
        this.countDues = this.countDues.bind(this);
    }

    componentDidMount() {
        this.countDues();
    }

    uploadReceipt () {
        let reader = new FileReader();
        console.log(this.state.bill[0]);
        reader.readAsDataURL(this.state.bill[0]);
        let title = this.state.title;
        let email = this.state.email;
        let participants = this.state.participants;
        reader.onloadend = function() {
            const base64data = reader.result;
            console.log(base64data);

            fetch('http://127.0.0.1:5000/bills/', {        //FIXME change port number
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    bill: base64data,
                    title: title,
                    email: email,
                    participants: participants,
                })
            })
        }
    }

    onFileChange (file) {
       this.setState({
            ...this.state,
            bill: file,
        })
    };

    countDues() {
        let email = this.state.email;

        fetch('http://127.0.0.1:5000/dues/', {        //FIXME change port number
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "due_from": email
            })
        }).then((response) => {this.setState({
            ...this.state,
            due: response.body})})
    }

    render() {
        const {classes, ...rest} = this.props;
        return (
            <div>
                <Header
                    color="primary"
                    routes={dashboardRoutes}
                    brand="SplitWise"
                    fixed
                    changeColorOnScroll={{
                        height: 400,
                        color: "white"
                    }}
                    {...rest}
                />
                <div className={classNames(classes.main, classes.mainRaised)}>
                    <div className={classes.container}>
                        <GridContainer justify="center">
                            <GridItem xs={12} sm={12} md={8}>
                                <CustomInput
                                    onChangeText={(title) => this.setState({
                                        ...this.state,
                                        title
                                    })}
                                    value={this.state.title}
                                    labelText={"Receipt title"}
                                />
                            </GridItem>
                            <GridItem xs={12} sm={12} md={8}>
                                <CustomInput
                                    onChangeText={(email) => this.setState({
                                        ...this.state,
                                        email
                                    })}
                                    value={this.state.email}
                                    labelText={"Payer email"}
                                />
                            </GridItem>
                            <GridItem xs={12} sm={12} md={8}>
                                <CustomInput
                                    onChangeText={(participants) => this.setState({
                                        ...this.state,
                                        participants: participants.split(',')
                                    })}
                                    value={this.state.email}
                                    labelText={"Participants (split with ',')"}
                                />
                            </GridItem>
                            <GridItem xs={5} sm={5} md={8}>
                                <div
                                ref={(el) => {
                                    if (el) {
                                    el.style.setProperty('background-color', "#DCDCDC", 'important');
                                    el.style.setProperty('width', "10em", 'important');
                                    }}}
                                >
                                    <Files
                                        onChange={this.onFileChange}
                                        accepts={['image/png']}
                                        maxFiles={1}
                                        maxFileSize={10000000}
                                        minFileSize={0}
                                        clickable
                                    >
                                        Click here to add bills
                                    </Files>
                                </div>
                            </GridItem>
                            <GridItem xs={12} sm={12} md={8}>
                                <Button onClick={this.uploadReceipt}>
                                    Upload receipt
                                </Button>
                            </GridItem>
                            <GridItem xs={12} sm={12} md={8}>
                                <Button onClick={this.countDues}>
                                    Count my dues
                                </Button>
                            </GridItem>
                            <GridItem xs={12} sm={12} md={8}>
                                <label>
                                    Your due:
                                    {this.state.due}
                                </label>
                            </GridItem>
                            <br/><br/>
                        </GridContainer>
                    </div>
                </div>
            </div>
        );
    }
}

export default withStyles(homePageStyle)(HomePage);
