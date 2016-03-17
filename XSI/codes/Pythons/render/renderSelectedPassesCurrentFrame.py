passes =  Application.Selection
currentFrame = Application.GetValue( 'PlayControl.Current' )
Application.RenderPasses( passes, currentFrame, currentFrame, 1 )