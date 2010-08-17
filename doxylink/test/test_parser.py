import unittest

from sphinxcontrib.doxylink import parsing

try:
	import cProfile as profile
except ImportError:
	import profile
   
import pstats

#List of tuples of: (input, correct output)
#Input is a string, output is a tuple.
arglists = [('( QUrl source )', ('', '(QUrl)')),
            ('( QUrl * source )', ('', '(QUrl*)')),
            ('( QUrl ** source )', ('', '(QUrl**)')),
            ('( const QUrl ** source )', ('', '(const QUrl**)')),
            ('( const QUrl source )', ('', '(const QUrl)')),
            ('( QUrl & source )', ('', '(QUrl&)')),
            ('( const QUrl & source )', ('', '(const QUrl&)')),
            ('( const QUrl * source )', ('', '(const QUrl*)')),
            ('( const QUrl const * source )', ('', '(const QUrl const *)')),
            ('( const QByteArray & data, const QUrl & documentUri = QUrl() )', ('', '(const QByteArray&, const QUrl&)')),
            ('(void)', ('', '(void)')),
            ('(uint32_t uNoOfBlocksToProcess=(std::numeric_limits< uint32_t >::max)())', ('', '(uint32_t)')),
            ('( QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = 0 )', ('', '(QWidget*, const char*, Qt::WindowFlags)')),
            ('()', ('', '()')),
            ('( const QPixmap & pixmap, const QString & text, int index = -1 )', ('', '(const QPixmap&, const QString&, int)')),
            ('( const char ** strings, int numStrings = -1, int index = -1 )', ('', '(const char**, int, int)')),
            ('( const QStringList & list, int index = -1 )', ('', '(const QStringList&, int)')),
            ('( int index = 0 )', ('', '(int)')),
            ('( bool ascending = true )', ('', '(bool)')),
            ('( const QIcon & icon, const QString & label, int width = -1 )', ('', '(const QIcon&, const QString&, int)')),
            ('( const QString & text, int column, ComparisonFlags compare = ExactMatch | Qt::CaseSensitive )', ('', '(const QString&, int, ComparisonFlags)')),
            ('( QWidget * parent = 0, const char * name = 0, Qt::WindowFlags f = Qt::WType_TopLevel )', ('', '(QWidget*, const char*, Qt::WindowFlags)')),
            ('( QMutex * mutex, unsigned long time = ULONG_MAX )', ('', '(QMutex*, unsigned long)')),
            ('( QReadWriteLock * readWriteLock, unsigned long time = ULONG_MAX )', ('', '(QReadWriteLock*, unsigned long)')),
            ('(const VolumeSampler< VoxelType > &volIter)', ('', '(const VolumeSampler< VoxelType >&)')),
            ('(VolumeSampler< VoxelType > &volIter)', ('', '(VolumeSampler< VoxelType >&)')),
            ('(const VolumeSampler< VoxelType > &volIter)', ('', '(const VolumeSampler< VoxelType >&)')),
            ('(const uint32_t(&pDimensions)[noOfDims])', ('', '(const uint32_t)')),
            ('(Array< noOfDims, ElementType > &rhs)', ('', '(Array< noOfDims, ElementType >&)')),
            ('( const QString & path, const QString & nameFilter, SortFlags sort = SortFlags( Name | IgnoreCase ))', ('', '(const QString&, const QString&, SortFlags)')),
            ('( GLuint texture_id )', ('', '(GLuint)')),
            ('( Q3ValueList<T>::size_type i )', ('', '(Q3ValueList< T >::size_type)')),
            ('(STLAllocator< T, P > const *, STLAllocator< T2, P > const &)', ('', '(STLAllocator< T, P > const *, STLAllocator< T2, P > const &)')),
            ('(STLAllocator< T, P > const &, STLAllocator< T2, P > const &)', ('', '(STLAllocator< T, P > const &, STLAllocator< T2, P > const &)')),
            ('(const String &errorMessage, String logName="")', ('', '(const String&, String)')),
            ('(PixelFormat = PF_BYTE)', ('', '(PixelFormat)')),
            ('(const SharedPtr< ControllerValue< T > > &src)', ('', '(const SharedPtr< ControllerValue < T > >&)')),
            ('(typename T::iterator start, typename T::iterator last)', ('', '(typename T::iterator, typename T::iterator)')),
            ('(const Matrix4 *const *blendMatrices)', ('', '(const Matrix4* const *)')),
            ('(int nb=0,...)', ('','(int, ...)')),
]

functions = [('PolyVox::Volume::getDepth', ('PolyVox::Volume::getDepth', '')),
             ('PolyVox::Volume::getDepth()', ('PolyVox::Volume::getDepth', '()')),
             ('Volume::getVoxelAt(uint16_t uXPos, uint16_t uYPos, uint16_t uZPos, VoxelType tDefault=VoxelType()) const', ('Volume::getVoxelAt', '(uint16_t, uint16_t, uint16_t, VoxelType) const')),
             ('PolyVox::Array::operator[]', ('PolyVox::Array::operator[]', '')),
             ('operator[]', ('operator[]', '')),
]

class TestNormalise(unittest.TestCase):
	def setUp(self):
		self.arglists = arglists
		self.functions = functions
	
	def test_split_function(self):
		for function in self.functions:
			self.assertEqual(parsing.normalise(function[0]), function[1])
			
	def test_normalise_arglist(self):
		for arglist in self.arglists:
			self.assertEqual(parsing.normalise(arglist[0]), arglist[1])
	
	def test_false_signatures(self):
		#This is an invalid function argument. Caused by a bug in Doxygen. See openbabel/src/ops.cpp : theOpCenter("center")
		from pyparsing import ParseException
		self.assertRaises(ParseException, parsing.normalise, '("center")')

if __name__ == "__main__":
	profile.runctx("for arglist in arglists: parsing.normalise(arglist[0])", globals(), locals(), filename='parsing_profile')
	p = pstats.Stats('parsing_profile')
	p.strip_dirs().sort_stats('cumulative').print_stats(20)

