import * as React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Image, View, Touchable, TouchableOpacity } from 'react-native';
import { Button, Provider as PaperProvider, Text, TextInput } from 'react-native-paper';

export default function App() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  function loginAttempt() {
    if (username === "sally") {
      setTest("logged in as patient");
    } else {
      setTest("incorrect username/password");
    }
  }

  return (
    <View style={styles.mainView}> 
    <View style={styles.TopView}>
        <Image source={require('./assets/mainlogo.png')} style={styles.logo} />
    </View>
      <View style={styles.BottomView}>
        <Image source={require('./assets/heading.png')} style={styles.Heading} />  
        <View style={styles.FormView}>
          <TextInput selectionColor={'black'} placeholder={"Username"} placeholderTextColor={'#000'} style={styles.TextInput} value={username} onChangeText={username => setUsername(username)}/>
          <TextInput selectionColor={'black'} placeholder={"Password"} secureTextEntry={true} placeholderTextColor={'#000'} style={styles.TextInput} value={password} onChangeText={password => setPassword(password)}/>
          <TouchableOpacity style={styles.Button}>
            <Text style={styles.ButtonText}>Sign in</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  mainView:{
    marginTop:40,
    flex:1,
    flexDirection:'column',
    justifyContent: 'center',
    alignItems: "center",
    backgroundColor:'#ffeed1',
  },
  TopView:{
    width:'100%',
    height:'40%',
    display:'flex',
    justifyContent:'center',
    alignItems:'center',
    backgroundColor:'#ffeed1',
  },
  BottomView:{
    width: '100%',
    height: '87%',
    backgroundColor:'#FFBA5D',
    borderTopLeftRadius:30,
    borderTopRightRadius:30
  },
  logo:{
    width:'60%',
    resizeMode:'contain',
    marginTop:20,
    marginLeft:-20
  },
  Heading:{
    resizeMode:'contain',
    width:'50%',
    marginTop:10,
    marginLeft:40,
  }, 
  FormView:{
    width: '100%',
    display:'flex',
    flexDirection:'column',
    alignItems:'center',
    marginTop:-20
  },
  TextInput:{
    width:'90%',
    borderWidth:4,
    height:52,
    borderRadius:10,
    paddingLeft:5,
    backgroundColor: "#9997",
    marginTop:20,
  },
  Button: {
    width:'90%',
    color:"#000",
    height:52,
    backgroundColor:'#000',
    borderRadius:10,
    marginTop:180,
    display:'flex',
    justifyContent:"center",
    alignItems:"center"
  },
  ButtonText:{
    fontWeight:'bold',
    fontSize:18,
    color:"#ffeed1"
  }



});