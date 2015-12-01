#Woo
from gettext import gettext as _
from gi.repository import Gtk, Gdk, Gio, GLib, GtkSource, Gedit, GObject
import signals , string , os


class GeditLineSuggesterPlugin( GObject.Object , Gedit.WindowActivatable ):

      __gtype_name__ = "GeditLineSuggester"
      window = GObject.property( type=Gedit.Window )
      global library
      library = {}
      global whitelist
      whitelist = [45 , 46 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 95 , 97 , 98 , 99 , 100 , 101 , 102 , 103 , 104 , 105 , 106 , 107 , 108 , 109 , 110 , 111 , 112 , 113 , 114 , 115 , 116 , 117 , 118 , 119 , 120 , 121 , 122 , 65456 , 65457 , 65458 , 65459 , 65460 , 65461 , 65462 , 65463 , 65464 , 65465 , 65505 , 65506 , 65509 ]
      
      def __init__( self ):
            GObject.Object.__init__( self )

      def do_activate( self ):
            pass

      def do_deactivate( self ):
            pass

      def do_update_state( self ):
            pass


class GeditLineSuggesterWindowActivatable( GObject.Object , Gedit.WindowActivatable ):
      
      __gtype_name__ = "GeditLineSuggesterActivatable"
      window = GObject.property( type = Gedit.Window )

      def __init__( self ):
            GObject.Object.__init__( self )
            
      def do_activate( self ):
            pass
            
      def do_deactivate( self ):
            pass
            
      def do_update_state( self ):
            pass
            
            
class GeditLineSuggesterViewActivatable( GObject.Object , Gedit.ViewActivatable , signals.Signals ):

      __gtype_name__ = "GeditLineSuggesterViewActivatable"
      view = GObject.property( type = Gedit.View )
      librarystrings = ""
      firstpress = True
      List = []
      
      def __init__( self ):
            GObject.Object.__init__( self )
            signals.Signals.__init__( self )
            langs = open( 'Languages.txt' , 'r' )
            for line in langs:
                  langname = line.find( "*" )
                  key = line[ 0:langname ]
                  val = line[ langname+1:-1 ]
                  if not key in library:
                        print ( "Adding language named:" , key )
                        library[key] = val.lower()
            langs.close()

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
            if event.keyval == 65289 and self.List != []:
                  self.insert( self.List[0] )
            elif event.keyval in whitelist:        
                  self.iteradv()
            else:
                  self.List = []
                  self.iterclear()
                  
      def mouse_press( self , view , event ):
            self.iterclear()

      def iteradv( self ):
            if self.firstpress:
                  self.firstpress = False
                  self.getlib()
            buf = self.view.get_buffer()
            buf.move_mark_by_name( "marktwo" , buf.get_iter_at_mark(buf.get_insert()) )
            markone = buf.get_iter_at_mark( buf.get_mark( "markone" ) )
            marktwo = buf.get_iter_at_mark( buf.get_mark( "marktwo" ) )
            search = buf.get_text( markone , marktwo , True ).lower()
            if search != "":
                  self.List = self.BoyerMooreSearch( search , self.librarystrings )
                  os.system('cls' if os.name == 'nt' else 'clear')
                  for member in self.List:
                         print ( member )
                  
                              
      def iterclear( self ):
            buf = self.view.get_buffer()
            buf.move_mark_by_name( "markone" , buf.get_iter_at_mark(buf.get_insert()) )
            buf.move_mark_by_name( "marktwo" , buf.get_iter_at_mark(buf.get_insert()) )
      
      def getlib( self ):
            buf = self.view.get_buffer()
            languages = buf.get_text( buf.get_start_iter() , buf.get_iter_at_line( 1 ), False )[:-1].lstrip( "#" ).split(",")
            print ( "Trying to load:" , languages )
            for keyword in languages:
                  if keyword in library: 
                        self.librarystrings += library[keyword]
                  else:
                        print ( "Language -" , keyword , "- is not in library." )
      
      def BoyerMooreSearch( self , search , lib ):
            search_len = len( search )-1
            tmp_strings = []
            pos = 0
            while 1:
                  pos = lib.find( search[search_len] , pos )
                  if lib.find( search , pos - len( search ) -1 , pos +1 ) != -1:
                        word = self.wordatpos( lib , pos )
                        if word != '':
                              tmp_strings.append( word )
                  elif pos == -1:
                        break
                  pos += 1
            return tmp_strings
            
      def wordatpos( self , lib , pos ):
            start = 0
            end = 0
            tmp = pos
            while lib[tmp-1] != ",":
                  tmp -= 1
            start = tmp
            tmp = pos
            while tmp < len(lib) and lib[tmp] != ",":
                  tmp += 1
            end = tmp
            return lib[start:end]
            
      def insert( self , string ):
            buf = self.view.get_buffer()
            buf.delete( buf.get_iter_at_mark(buf.get_mark( "markone" )) , buf.get_iter_at_mark(buf.get_insert()) )
            buf.insert( buf.get_iter_at_mark(buf.get_mark( "markone" )) , string )
      
      
      
      
      
      
      
            
