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
        this.state = {
            image:0
        };
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
                transform: [{translate: [0, 0, -8]}],

            }
            ,button2: { 
                margin: 0.05, 
                height: 0.4, 
                transform: [{translate: [0, 0, 8]},{rotateY : -180}],

                
            }
            , text: { 
                width:1,
                height:1,
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
            if (newImage>=0){
                return {image:newImage}
            }
            else{
                return {image:prevState.image}
            }
            
        })
        console.log(this.state.image)
    }
    displaymoveForward=()=>{
    
            return(
                <VrButton style={this.styles.button} 
                    onClick={() => this.moveForward()}> 
   
                    <Image
                              style={this.styles.text}
                              source={require('./forward.png')}
                            />
                    </VrButton>
            );
        
    }
    displaymoveBack=()=>{
        if(this.state.image!==0){
            return(
                <VrButton  style={this.styles.button,this.styles.button2} 
                onClick={() => this.moveBack()}> 
                <Image
                              style={this.styles.text}
                              source={require('./forward.png')}
                            />
                </VrButton> 
            );
        }
    }


  render() {
    return (
            <View>
        <Pano 
            source={asset(`result${this.state.image}.jpg`)}
            />
                {this.displaymoveForward()}
                {this.displaymoveBack()}
                

      </View>
    );
  }
};

AppRegistry.registerComponent('streetViewDev', () => streetViewDev);





//
//
//moveForward(){
//        console.log(this.state.image)
//        if(this.state.displaymoveForward-this.state.image!==0){
//            this.setState(prevState=>{
//                let newImage = prevState.image + 1;
//                if(newImage){
//                    return {
//                        image:newImage
//                }
//            }})
//        }
//        console.log(this.state.image)
//    }
//    moveForwardCheck=()=>{
//        fetch(`/static_assets/result${this.state.image+1}.jpg`).then((resp)=>{
//            console.log(resp)
//            if(resp.status == 200){
//                this.setState((prevState)=>{
//                return{
//                    displaymoveForward: this.state.image+1,
//                }
//            })
//            }else{
//                console.log("404")
//            }
//        },(error) =>{
//            console.log("error")
//            console.log(resp)
//        })
//    }
//    
