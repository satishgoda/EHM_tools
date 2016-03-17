Select your hair object and run. It creates one curve by guide.
If you need to merge some of the curves, you will need an other script ( I send it to the list some time ago).

//***************************************
var xHair = Selection(0);

HairPointsValues( xHair )


function HairPointsValues( xHair )
{
                
        var PointsPerGuideHair = 14 ; // This is always true
        var valuesPerPosition = 3 ; // x,y,z
        var gHair = xHair.ActivePrimitive.Geometry;
        var aAllPositions = gHair.Points.PositionArray.toArray();

        var cntGuideHairs = aAllPositions.length / ( valuesPerPosition * PointsPerGuideHair ) ;
        var oMesh = HairPolymesh(xHair); 
        var oPoints = oMesh.Geometry.Points;

        for ( i = 0 ; i < cntGuideHairs ; i++ )
        {
                var posArray = new Array();
                
                var oHairRootx = oPoints.item(i).position.x;
                var oHairRooty = oPoints.item(i).position.y;
                var oHairRootz = oPoints.item(i).position.z;
                
                logmessage("guide n : "+i);

                posArray.push(oHairRootx);
                posArray.push(oHairRooty);
                posArray.push(oHairRootz);
                posArray.push(1);

                indexHairRoot = i * valuesPerPosition * PointsPerGuideHair ;
                
                
                
                for ( k = 0 ; k < PointsPerGuideHair ; k++ )
                {                                        
                        xIndex = k*valuesPerPosition + indexHairRoot ;
                        posArray.push( aAllPositions[xIndex ]);
                        posArray.push( aAllPositions[xIndex + 1]);
                        posArray.push( aAllPositions[xIndex + 2]);
                        posArray.push( 1 );
                }
                var degrees = [1];
                var params = [siUniformParameterization];
                var closed = [false];
                var initCurve = ActivesceneRoot.AddNurbsCurveList2(1, posArray, null, null, null, closed, degrees, params, siSINurbs, "LinesFromGuides" );
        }


// return the geometry source
function HairPolymesh(HairObject)
{
        //Find the hair operator.
        oEnum = new Enumerator( HairObject.ActivePrimitive.ConstructionHistory );
        for (;!oEnum.atEnd();oEnum.moveNext())
        {
                if( oEnum.item().name == "Hair Generator Operator" )
                {
                        oOp = oEnum.item();
                        oEnumInPort = new Enumerator( oOp.InputPorts ) ;
                        for (;!oEnumInPort.atEnd();oEnumInPort.moveNext() )
                        {
                                var oInPort = oEnumInPort.item () ;
                                if(oInPort.GroupName == "Group_0")
                                {
                                        var oMesh = oInPort.Target2;
                                        return oMesh;
                                }
                        }
                }
        }
}

//***********************************************

Cheers !

--
Guillaume Laforge | La Maison

PS : If you use Linux you must add those line before the script :

// Add a push method to the JScript Array Object
// @cc_on
// @if (@_jscript_version < 5.5)
var push = function(){
        for( var i = 0; arguments[ i ] != null; i++ )
                this[this.length++] = arguments[ i ];
        return( this );
        }
Array.prototype.push = push;
// @end

On Thu, 3 Jan 2008 15:19:13 -0500, "Marc-Andre Carbonneau" <marc-andre...@ubisoft.com> wrote:
> Heya!
> 
>  
> 
> First, Happy New Year! Wish you all the best for 2008. Lots of exciting
> projects for you all I'm sure!
> 
>  
> 
> My TD is still on holyday so could anyone help me convert hair to
> curves? Anyone wrote such a script or plu

---
Unsubscribe? Mail Majordomo@Softimage.COM with the following text in body:
unsubscribe xsi

 


Guillaume Laforge 	
1/3/08
Other recipients: X...@softimage.com


And here is the script to merge the curves (all the curves are merged in the first selected curve):
var my_crvlist = Selection(0).ActivePrimitive.Geometry;

for ( var i=1;i<Selection.count;i++ )
{
        var obj = Selection(i);
        var crvlist = obj.ActivePrimitive.Geometry;
        var crv = crvlist.Curves(0);

        var VBdata = crv.Get2( siSiNurbs ); 
        var data = VBdata.toArray();

        var crtlvertices = data[0];
        var knots = data[1];
        var isclosed = data[2];
        var degree = data[3];
        var parameterization = data[4];

        var newcrv = my_crvlist.AddCurve( crtlvertices, knots, isclosed, degree, parameterization );