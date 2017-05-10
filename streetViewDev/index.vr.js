import React from 'react';

import {
  AppRegistry,
  asset,
  StyleSheet,
  Pano,
  Text,
  View,
    VrButton,
    Image
} from 'react-vr';


export default class streetViewDev extends React.Component {
    constructor(){
        super();
        this.state = {image:1};
        this.styles = StyleSheet.create({ 
            menu: { flex: 1, 
                   flexDirection: 'column', 
                   width: 1, 
                   alignItems: 'stretch', 
                   transform: [{translate: [0, 0, -5]}],
            }
            ,button: { 
                margin: 0.05, 
                height: 0.4, 
                backgroundColor:"rgba(255,0,0,0.1)",
                transform: [{translate: [0, 0, -5]}],

            }
            ,button2: { 
                margin: 0.05, 
                height: 0.4, 
                backgroundColor:"rgba(0,255,0,0.1)",
                transform: [{translate: [0, 0, 5]},{rotateY : -180}],

                
            }
            , text: { 
                fontSize: 0.3, 
                color:"#fff",
                textAlign: 'center', 
            }, 
        
        });
    };
    moveForward(){
        console.log(this.state.image)
        this.setState(prevState=>{
            let newImage = prevState.image + 1;
            if(newImage){
            return {image:newImage}
            }
        })
        console.log(this.state.image)
    }
    moveBack(){
        console.log(this.state.image)
        this.setState(prevState=>{
            let newImage = prevState.image - 1;
            if (newImage>0){
                return {image:newImage}
            }
            else{
                return {image:prevState.image}
            }
            
        })
        console.log(this.state.image)
    }
  render() {
    return (
            <View>
        <Pano source={asset(`result${this.state.image}.jpg`)}/>

                <VrButton style={this.styles.button} 
                onClick={() => this.moveForward()}> 
                <Text style={this.styles.text}> 
                    Do przodu! </Text> 
                </VrButton>
                <VrButton  style={this.styles.button,this.styles.button2} 
                onClick={() => this.moveBack()}> 
                <Text style={this.styles.text}> 
                    Do tyłu! </Text> 
                </VrButton> 

      </View>
    );
  }
};

AppRegistry.registerComponent('streetViewDev', () => streetViewDev);
