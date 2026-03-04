import QtQuick3D
import QtQuick3D.AssetUtils
import QtQuick3D.Helpers
import QtQuick3D.Particles3D
import QtQuick3D.Xr
import QtQuick
import QtQuick3D.Helpers

View3D {
    id: blochview
    anchors.fill: parent
    camera: cameraNode

    property int theta: 45
    property int phi: 45

    environment: SceneEnvironment {
        clearColor: "#112220"
    }

    Node {
        id: originNode
        PerspectiveCamera {
            id: cameraNode
            z: 300
        }

        DirectionalLight {
            z: 400
            brightness: 100
        }
    }
    
    Node {
        Model {
            source: "#Sphere"
            scale: Qt.vector3d(2, 2, 2)
            opacity: 0.5

            materials: DefaultMaterial {
                diffuseColor: "black"
                opacity: 0.2
            }
        }


        Text {
            font.family: "Noto Sans Mono"
            text: "|1⟩"
            y: -125
        }

        Text {

            font.family: "Noto Sans Mono"
            text: "|0⟩"
            y: 100
        }
    }

    Node {

        eulerRotation: Qt.vector3d(blochview.phi, blochview.theta, 0)
        
        Model {

            source: "#Cylinder"
            scale: Qt.vector3d(0.225, 0.75, 0.225)
            
            position.y: 40
            materials: DefaultMaterial {
                diffuseColor: "black"
                opacity: 0.8
            }

            Model {
                source: "#Cone"
                scale: Qt.vector3d(1.25, 0.5, 1.25)
                position.y: 50
                materials: DefaultMaterial {
                    diffuseColor: "black"
                    opacity: 0.8
                }
            }
        }
    }

    AxisHelper {
        enableAxisLines: false
        enableXYGrid: true
    }

    OrbitCameraController {
        origin: originNode
        camera: cameraNode
    }
}
