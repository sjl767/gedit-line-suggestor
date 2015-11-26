from gettext import gettext as _
from gi.repository import Gtk, Gdk, Gio, GLib, GtkSource, Gedit, GObject
import signals , string


class GeditLineSuggesterPlugin( GObject.Object , Gedit.WindowActivatable ):

      __gtype_name__ = "GeditLineSuggester"
      window = GObject.property(type=Gedit.Window)
      global whitelist
      whitelist = [45 , 46 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 95 , 97 , 98 , 99 , 100 , 101 , 102 , 103 , 104 , 105 , 106 , 107 , 108 , 109 , 110 , 111 , 112 , 113 , 114 , 115 , 116 , 117 , 118 , 119 , 120 , 121 , 122 , 65456 , 65457 , 65458 , 65459 , 65460 , 65461 , 65462 , 65463 , 65464 , 65465 , 65505 , 65506 , 65509 ]
      
      def __init__(self):
            GObject.Object.__init__(self)

      def do_activate(self):
            pass

      def do_deactivate(self):
            pass

      def do_update_state(self):
            pass


class GeditLineSuggesterWindowActivatable( GObject.Object , Gedit.WindowActivatable ):
      
      __gtype_name__ = "GeditLineSuggesterActivatable"
      window = GObject.property(type=Gedit.Window)
      global library
      library = {}

      def __init__(self):
            GObject.Object.__init__(self)

      def do_activate( self ):
            langs = open( 'Languages.txt' , 'r' )
            membs = 0
            for line in langs:
                  langname = line.find( "*" )
                  key = line[ 0:langname ]
                  val = line[ langname+1: ]
                  print ( "Adding language named:" , key )
                  if not key in library:
                        library[key] = val
                  print ( library["Woo"] )
            langs.close()
            
      def do_deactivate( self ):
            pass
            
      def do_update_state( self ):
            pass
            
            
class GeditLineSuggesterViewActivatable( GObject.Object , Gedit.ViewActivatable , signals.Signals ):

      __gtype_name__ = "GeditLineSuggesterViewActivatable"
      view = GObject.property( type = Gedit.View )
      
      def __init__( self ):
            GObject.Object.__init__( self )
            signals.Signals.__init__(self)

      def do_activate( self ):
            self.connect_signal( self.view , 'key-release-event' , self.key_release )
            self.connect_signal( self.view , 'button-release-event' , self.mouse_press )
            buf = self.view.get_buffer()
            buf.create_mark( "markone" , buf.get_start_iter() , True )
            buf.create_mark( "marktwo" , buf.get_start_iter() , True )
            
      def do_deactivate( self ):
            pass
            
      def do_update_state( self ):
            pass
      
      def key_release( self , view , event ):
            if event.keyval in whitelist:        
                  self.iteradv()
            else:
                  self.iterclear()
                  
      def mouse_press( self , view , event ):
            self.iterclear()
      
      def iteradv( self ):
            buf = self.view.get_buffer()
            buf.move_mark_by_name( "marktwo" , buf.get_iter_at_mark(buf.get_insert()) )
            markone = buf.get_iter_at_mark(buf.get_mark("markone"))
            marktwo = buf.get_iter_at_mark(buf.get_mark("marktwo"))
            print ( buf.get_text( markone , marktwo , True ) )
                              
      def iterclear( self ):
            buf = self.view.get_buffer()
            buf.move_mark_by_name( "markone" , buf.get_iter_at_mark(buf.get_insert()) )
            buf.move_mark_by_name( "marktwo" , buf.get_iter_at_mark(buf.get_insert()) )


