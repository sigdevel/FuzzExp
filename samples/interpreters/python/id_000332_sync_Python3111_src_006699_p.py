



"""
Unit tests for the OpenVDB Python module

These are intended primarily to test the Python-to-C++ and
C++-to-Python bindings, not the OpenVDB library itself.
"""

import os, os.path
import sys
import unittest
import inspect


if 'add_dll_directory' in dir(os):
    
    config = os.path.basename(os.getcwd())
    os.add_dll_directory(os.getcwd() + '\\..\\..\\' + config)
    if os.getenv('OPENVDB_TEST_PYTHON_AX'):
        os.add_dll_directory(os.getcwd() +
            '\\..\\..\\..\\..\\openvdb_ax\\openvdb_ax\\' + config)

import pyopenvdb as openvdb


def valueFactory(zeroValue, elemValue):
    """
    Return elemValue converted to a value of the same type as zeroValue.
    If zeroValue is a sequence, return a sequence of the same type and length,
    with each element set to elemValue.
    """
    val = zeroValue
    typ = type(val)
    try:
        
        size = len(val)
        val = typ([elemValue]) * size
    except TypeError:
        
        val = typ(elemValue)
    return val


def ax_is_enabled():
    '''
    Return true if we should be testing pyopenvdb.ax(). This environment
    variable is set by the CMake test command if we expect AX to be tested.
    '''
    ax_hook_exists = 'ax' in dir(openvdb) and inspect.isbuiltin(openvdb.ax)
    ax_is_enabled = os.getenv('OPENVDB_TEST_PYTHON_AX')
    if ax_is_enabled and not ax_hook_exists:
        raise RuntimeError('Expected to test the AX python hooks but '
            'pyopenvdb.ax() has not been located.')
    return ax_is_enabled


class TestOpenVDB(unittest.TestCase):

    def run(self, result=None, *args, **kwargs):
        super(TestOpenVDB, self).run(result, *args, **kwargs)

    def setUp(self):
        
        self.umask = os.umask(0)

    def tearDown(self):
        os.umask(self.umask)


    def testModule(self):
        
        self.assertTrue(openvdb.BoolGrid in openvdb.GridTypes)
        self.assertTrue(openvdb.FloatGrid in openvdb.GridTypes)
        self.assertTrue(openvdb.Vec3SGrid in openvdb.GridTypes)

        
        for cls in openvdb.GridTypes:
            grid = cls()
            acc = grid.getAccessor()
            acc.setValueOn((-1, -2, 3))
            self.assertEqual(grid.activeVoxelCount(), 1)


    def testAX(self):
        if not ax_is_enabled():
            return

        float_grid = openvdb.FloatGrid()
        float_grid.name = 'float_grid'
        ijk = (1, 1, 1)

        acc = float_grid.getAccessor()
        acc.setValueOn((ijk))
        self.assertEqual(acc.getValue(ijk), 0)

        openvdb.ax('@float_grid = 2;', float_grid)
        self.assertEqual(acc.getValue(ijk), 2)
        acc.setValueOn((ijk))

        float_grid.fill((0, 0, 0), (7, 7, 7), -1, active=True)
        openvdb.ax('@float_grid = lengthsq(getcoord());', float_grid)

        for i in range(0, 8):
            for j in range(0, 8):
                for k in range(0, 8):
                    ijk = (i, j, k)
                    lsq = (i*i)+(j*j)+(k*k)
                    self.assertEqual(acc.getValue(ijk), lsq)

        vec3_grid = openvdb.Vec3SGrid()
        vec3_grid.name = 'vec_grid'

        vec3_grid.fill((0, 0, 0), (7, 7, 7), (-1,-1,-1), active=True)
        openvdb.ax('v@vec_grid = @float_grid;', [vec3_grid, float_grid])
        acc = vec3_grid.getAccessor()

        for i in range(0, 8):
            for j in range(0, 8):
                for k in range(0, 8):
                    ijk = (i, j, k)
                    lsq = (i*i)+(j*j)+(k*k)
                    self.assertEqual(acc.getValue(ijk), (lsq,lsq,lsq))


    def testTransform(self):
        xform1 = openvdb.createLinearTransform(
            [[.5,  0,  0,  0],
             [0,   1,  0,  0],
             [0,   0,  2,  0],
             [1,   2,  3,  1]])
        self.assertTrue(xform1.typeName != '')
        self.assertEqual(xform1.indexToWorld((1, 1, 1)), (1.5, 3, 5))
        xform2 = xform1
        self.assertEqual(xform2, xform1)
        xform2 = xform1.deepCopy()
        self.assertEqual(xform2, xform1)
        xform2 = openvdb.createFrustumTransform(taper=0.5, depth=100,
            xyzMin=(0, 0, 0), xyzMax=(100, 100, 100), voxelSize=0.25)
        self.assertNotEqual(xform2, xform1)
        worldp = xform2.indexToWorld((10, 10, 10))
        worldp = [int(round(x * 1000000)) for x in worldp]
        self.assertEqual(worldp, [-110000, -110000, 2500000])

        grid = openvdb.FloatGrid()
        self.assertEqual(grid.transform, openvdb.createLinearTransform())
        grid.transform = openvdb.createLinearTransform(2.0)
        self.assertEqual(grid.transform, openvdb.createLinearTransform(2.0))


    def testGridCopy(self):
        grid = openvdb.FloatGrid()
        self.assertTrue(grid.sharesWith(grid))
        self.assertFalse(grid.sharesWith([])) 

        copyOfGrid = grid.copy()
        self.assertTrue(copyOfGrid.sharesWith(grid))

        deepCopyOfGrid = grid.deepCopy()
        self.assertFalse(deepCopyOfGrid.sharesWith(grid))
        self.assertFalse(deepCopyOfGrid.sharesWith(copyOfGrid))


    def testGridProperties(self):
        expected = {
            openvdb.BoolGrid:  ('bool',   False,      True),
            openvdb.FloatGrid: ('float',  0.0,        1.0),
            openvdb.Vec3SGrid: ('vec3s',  (0, 0, 0),  (-1, 0, 1)),
        }

        for factory in expected:
            valType, bg, newbg = expected[factory]

            grid = factory()

            self.assertEqual(grid.valueTypeName, valType)
            def setValueType(obj):
                obj.valueTypeName = 'double'
            
            self.assertRaises(AttributeError, lambda obj=grid: setValueType(obj))

            self.assertEqual(grid.background, bg)
            grid.background = newbg
            self.assertEqual(grid.background, newbg)

            self.assertEqual(grid.name, '')
            grid.name = 'test'
            self.assertEqual(grid.name, 'test')

            self.assertFalse(grid.saveFloatAsHalf)
            grid.saveFloatAsHalf = True
            self.assertTrue(grid.saveFloatAsHalf)

            self.assertTrue(grid.treeDepth > 2)


    def testGridMetadata(self):
        grid = openvdb.BoolGrid()

        self.assertEqual(grid.metadata, {})

        meta = {
            'name':     'test',
            'xyz':      (-1, 0, 1),
            'xyzw':     (1.0, 2.25, 3.5, 4.0),
            'intval':   42,
            'floatval': 1.25,
            'mat4val':  [[1]*4]*4,
            'saveFloatAsHalf': True,
        }
        grid.metadata = meta
        self.assertEqual(grid.metadata, meta)

        meta['xyz'] = (-100, 100, 0)
        grid.updateMetadata(meta)
        self.assertEqual(grid.metadata, meta)

        self.assertEqual(set(grid.iterkeys()), set(meta.keys()))

        for name in meta:
            self.assertTrue(name in grid)
            self.assertEqual(grid[name], meta[name])
            self.assertEqual(type(grid[name]), type(meta[name]))

        for name in grid:
            self.assertTrue(name in grid)
            self.assertEqual(grid[name], meta[name])
            self.assertEqual(type(grid[name]), type(meta[name]))

        self.assertTrue('xyz' in grid)
        del grid['xyz']
        self.assertFalse('xyz' in grid)
        grid['xyz'] = meta['xyz']
        self.assertTrue('xyz' in grid)

        grid.addStatsMetadata()
        meta = grid.getStatsMetadata()
        self.assertEqual(0, meta["file_voxel_count"])


    def testGridFill(self):
        grid = openvdb.FloatGrid()
        acc = grid.getAccessor()
        ijk = (1, 1, 1)

        self.assertRaises(TypeError, lambda: grid.fill("", (7, 7, 7), 1, False))
        self.assertRaises(TypeError, lambda: grid.fill((0, 0, 0), "", 1, False))
        self.assertRaises(TypeError, lambda: grid.fill((0, 0, 0), (7, 7, 7), "", False))

        self.assertFalse(acc.isValueOn(ijk))
        grid.fill((0, 0, 0), (7, 7, 7), 1, active=False)
        self.assertEqual(acc.getValue(ijk), 1)
        self.assertFalse(acc.isValueOn(ijk))

        grid.fill((0, 0, 0), (7, 7, 7), 2, active=True)
        self.assertEqual(acc.getValue(ijk), 2)
        self.assertTrue(acc.isValueOn(ijk))

        activeCount = grid.activeVoxelCount()
        acc.setValueOn(ijk, 2.125)
        self.assertEqual(grid.activeVoxelCount(), activeCount)

        grid.fill(ijk, ijk, 2.125, active=True)
        self.assertEqual(acc.getValue(ijk), 2.125)
        self.assertTrue(acc.isValueOn(ijk))
        self.assertEqual(grid.activeVoxelCount(), activeCount)
        leafCount = grid.leafCount()

        grid.prune()
        self.assertAlmostEqual(acc.getValue(ijk), 2.125)
        self.assertTrue(acc.isValueOn(ijk))
        self.assertEqual(grid.leafCount(), leafCount)
        self.assertEqual(grid.activeVoxelCount(), activeCount)

        grid.prune(tolerance=0.2)
        self.assertEqual(grid.activeVoxelCount(), activeCount)
        self.assertEqual(acc.getValue(ijk), 2.0) 
        self.assertTrue(acc.isValueOn(ijk))
        self.assertTrue(grid.leafCount() < leafCount)


    def testGridIterators(self):
        onCoords = set([(-10, -10, -10), (0, 0, 0), (1, 1, 1)])

        for factory in openvdb.GridTypes:
            grid = factory()
            acc = grid.getAccessor()
            for c in onCoords:
                acc.setValueOn(c)

            coords = set(value.min for value in grid.iterOnValues())
            self.assertEqual(coords, onCoords)

            n = 0
            for _ in grid.iterAllValues():
                n += 1
            for _ in grid.iterOffValues():
                n -= 1
            self.assertEqual(n, len(onCoords))

            grid = factory()
            grid.fill((0, 0, 1), (18, 18, 18), grid.oneValue) 
            activeCount = grid.activeVoxelCount()

            
            
            count = 0
            for value in grid.citerOnValues():
                count += value.count
            self.assertEqual(count, activeCount)

            
            
            state = True
            for value in grid.iterOnValues():
                count -= value.count
                value.active = state
                state = not state
            self.assertEqual(grid.activeVoxelCount(), activeCount / 2)

            
            value = grid.citerOnValues().next()
            self.assertRaises(AttributeError, lambda: setattr(value, 'active', 0))
            self.assertRaises(AttributeError, lambda: setattr(value, 'depth', 0))
            
            value = grid.iterOnValues().next()
            self.assertRaises(AttributeError, lambda: setattr(value, 'min', (0, 0, 0)))
            self.assertRaises(AttributeError, lambda: setattr(value, 'max', (0, 0, 0)))
            self.assertRaises(AttributeError, lambda: setattr(value, 'count', 1))


    def testMap(self):
        grid = openvdb.BoolGrid()
        grid.fill((-4, -4, -4), (5, 5, 5), grid.zeroValue) 
        grid.mapOn(lambda x: not x) 
        n = sum(item.value for item in grid.iterOnValues())
        self.assertEqual(n, 10 * 10 * 10)

        grid = openvdb.FloatGrid()
        grid.fill((-4, -4, -4), (5, 5, 5), grid.oneValue)
        grid.mapOn(lambda x: x * 2)
        n = sum(item.value for item in grid.iterOnValues())
        self.assertEqual(n, 10 * 10 * 10 * 2)

        grid = openvdb.Vec3SGrid()
        grid.fill((-4, -4, -4), (5, 5, 5), grid.zeroValue)
        grid.mapOn(lambda x: (0, 1, 0))
        n = sum(item.value[1] for item in grid.iterOnValues())
        self.assertEqual(n, 10 * 10 * 10)


    def testValueAccessor(self):
        coords = set([(-10, -10, -10), (0, 0, 0), (1, 1, 1)])

        for factory in openvdb.GridTypes:
            
            if factory.valueTypeName.startswith('ptdataidx'):
                continue
            grid = factory()
            zero, one = grid.zeroValue, grid.oneValue
            acc = grid.getAccessor()
            cacc = grid.getConstAccessor()
            leafDepth = grid.treeDepth - 1

            self.assertRaises(TypeError, lambda: cacc.setValueOn((5, 5, 5), zero))
            self.assertRaises(TypeError, lambda: cacc.setValueOff((5, 5, 5), zero))
            self.assertRaises(TypeError, lambda: cacc.setActiveState((5, 5, 5), True))
            self.assertRaises(TypeError, lambda: acc.setValueOn("", zero))
            self.assertRaises(TypeError, lambda: acc.setValueOff("", zero))
            if grid.valueTypeName != "bool":
                self.assertRaises(TypeError, lambda: acc.setValueOn((5, 5, 5), object()))
                self.assertRaises(TypeError, lambda: acc.setValueOff((5, 5, 5), object()))

            for c in coords:
                grid.clear()

                
                self.assertEqual(acc.getValue(c), zero)
                self.assertEqual(cacc.getValue(c), zero)
                self.assertFalse(acc.isValueOn(c))
                self.assertFalse(cacc.isValueOn(c))
                self.assertEqual(acc.getValueDepth(c), -1)
                self.assertEqual(cacc.getValueDepth(c), -1)

                acc.setValueOn(c) 
                self.assertEqual(acc.getValue(c), zero)
                self.assertEqual(cacc.getValue(c), zero)
                self.assertTrue(acc.isValueOn(c))
                self.assertTrue(cacc.isValueOn(c))
                self.assertEqual(acc.getValueDepth(c), leafDepth)
                self.assertEqual(cacc.getValueDepth(c), leafDepth)

                acc.setValueOff(c, grid.oneValue) 
                self.assertEqual(acc.getValue(c), one)
                self.assertEqual(cacc.getValue(c), one)
                self.assertFalse(acc.isValueOn(c))
                self.assertFalse(cacc.isValueOn(c))
                self.assertEqual(acc.getValueDepth(c), leafDepth)
                self.assertEqual(cacc.getValueDepth(c), leafDepth)

            
            
            def scoped():
                grid = factory()
                acc = grid.getAccessor()
                cacc = grid.getConstAccessor()
                one = grid.oneValue
                acc.setValueOn((0, 0, 0), one)
                del grid
                self.assertEqual(acc.getValue((0, 0, 0)), one)
                self.assertEqual(cacc.getValue((0, 0, 0)), one)
            scoped()


    def testValueAccessorCopy(self):
        xyz = (0, 0, 0)
        grid = openvdb.BoolGrid()

        acc = grid.getAccessor()
        self.assertEqual(acc.getValue(xyz), False)
        self.assertFalse(acc.isValueOn(xyz))

        copyOfAcc = acc.copy()
        self.assertEqual(copyOfAcc.getValue(xyz), False)
        self.assertFalse(copyOfAcc.isValueOn(xyz))

        
        acc.setValueOn(xyz, True)
        self.assertEqual(acc.getValue(xyz), True)
        self.assertTrue(acc.isValueOn(xyz))
        self.assertEqual(copyOfAcc.getValue(xyz), True)
        self.assertTrue(copyOfAcc.isValueOn(xyz))

        copyOfAcc.setValueOff(xyz)
        self.assertEqual(acc.getValue(xyz), True)
        self.assertFalse(acc.isValueOn(xyz))
        self.assertEqual(copyOfAcc.getValue(xyz), True)
        self.assertFalse(copyOfAcc.isValueOn(xyz))

        
        
        xyz2 = (-1, -1, -1)
        copyOfAcc.setValueOn(xyz2)
        self.assertTrue(copyOfAcc.isCached(xyz2))
        self.assertFalse(copyOfAcc.isCached(xyz))
        self.assertTrue(acc.isCached(xyz))
        self.assertFalse(acc.isCached(xyz2))


    def testPickle(self):
        import pickle

        
        testXforms = [
            openvdb.createLinearTransform(voxelSize=0.1),
            openvdb.createLinearTransform(matrix=[[1,0,0,0],[0,2,0,0],[0,0,3,0],[4,3,2,1]]),
            openvdb.createFrustumTransform((0,0,0), (10,10,10), taper=0.8, depth=10.0),
        ]
        for xform in testXforms:
            s = pickle.dumps(xform)
            restoredXform = pickle.loads(s)
            self.assertEqual(restoredXform, xform)

        
        for factory in openvdb.GridTypes:

            
            grid = factory()
            
            meta = { 'name': 'test', 'saveFloatAsHalf': True, 'xyz': (-1, 0, 1) }
            grid.metadata = meta
            
            active = True
            for width in range(63, 0, -10):
                val = valueFactory(grid.zeroValue, width)
                grid.fill((0, 0, 0), (width,)*3, val, active)
                active = not active

            
            s = pickle.dumps(grid)
            restoredGrid = pickle.loads(s)

            
            self.assertEqual(restoredGrid.metadata, meta)

            
            for restored, original in zip(restoredGrid.iterOnValues(), grid.iterOnValues()):
                self.assertEqual(restored, original)
            
            for restored, original in zip(restoredGrid.iterOffValues(), grid.iterOffValues()):
                self.assertEqual(restored, original)


    def testGridCombine(self):
        
        aGrid, bGrid = openvdb.FloatGrid(), openvdb.FloatGrid(background=1.0)
        for width in range(63, 1, -10):
            aGrid.fill((0, 0, 0), (width,)*3, width)
            bGrid.fill((0, 0, 0), (width,)*3, 2 * width)

        
        copyOfAGrid = aGrid.deepCopy()

        
        
        
        
        
        aGrid.combine(bGrid, lambda a, b: 2 * min(a, b) + 3 * max(a, b))

        self.assertTrue(bGrid.empty())

        
        for original, combined in zip(copyOfAGrid.iterOnValues(), aGrid.iterOnValues()):
            self.assertEqual(combined.min, original.min)
            self.assertEqual(combined.max, original.max)
            self.assertEqual(combined.depth, original.depth)
            self.assertEqual(combined.value, 8 * original.value)
        for original, combined in zip(copyOfAGrid.iterOffValues(), aGrid.iterOffValues()):
            self.assertEqual(combined.min, original.min)
            self.assertEqual(combined.max, original.max)
            self.assertEqual(combined.depth, original.depth)
            self.assertEqual(combined.value, 3)


    def testLevelSetSphere(self):
        HALF_WIDTH = 4
        sphere = openvdb.createLevelSetSphere(halfWidth=HALF_WIDTH, voxelSize=1.0, radius=100.0)
        lo, hi = sphere.evalMinMax()
        self.assertTrue(lo >= -HALF_WIDTH)
        self.assertTrue(hi <= HALF_WIDTH)


    def testCopyFromArray(self):
        import random
        import time

        
        try:
            import numpy as np
        except ImportError:
            return

        
        arr = np.zeros((1, 2, 1))
        grid = openvdb.FloatGrid()
        try:
            grid.copyFromArray(arr)
        except NotImplementedError:
            return

        
        grid = openvdb.FloatGrid()
        self.assertRaises(TypeError, lambda: grid.copyFromArray('abc'))
        arr = np.zeros((1, 2))
        self.assertRaises(ValueError, lambda: grid.copyFromArray(arr))

        
        arr = np.zeros((1, 2, 1), dtype = complex)
        grid = openvdb.FloatGrid()
        self.assertRaises(TypeError, lambda: grid.copyFromArray(arr))

        ARRAY_DIM = 201
        BG, FG = 0, 1

        
        random.seed(0)
        def randCoord():
            return tuple(random.randint(0, ARRAY_DIM-1) for i in range(3))
        coords = set(randCoord() for i in range(200))

        def createArrays():
            
            for shape in (
                (ARRAY_DIM, ARRAY_DIM, ARRAY_DIM),      
                (ARRAY_DIM, ARRAY_DIM, ARRAY_DIM, 3)    
            ):
                for dtype in (np.float32, np.int32, np.float64, np.int64, np.uint32, np.bool):
                    
                    
                    arr = np.ndarray(shape, dtype)
                    arr.fill(BG)
                    bg = arr[0, 0, 0]
                    for c in coords:
                        arr[c] = FG

                    yield arr

        
        for cls in openvdb.GridTypes:
            
            if cls.valueTypeName.startswith('ptdataidx'):
                continue
            for arr in createArrays():
                isScalarArray = (len(arr.shape) == 3)
                isScalarGrid = False
                try:
                    len(cls.zeroValue) 
                except TypeError:
                    isScalarGrid = True 

                gridBG = valueFactory(cls.zeroValue, BG)
                gridFG = valueFactory(cls.zeroValue, FG)

                
                grid = cls(gridBG)
                acc = grid.getAccessor()

                
                
                if isScalarGrid != isScalarArray:
                    self.assertRaises(ValueError, lambda: grid.copyFromArray(arr))
                    continue

                
                
                
                grid.copyFromArray(arr)
                
                
                
                
                

                
                self.assertEqual(grid.activeVoxelCount(), len(coords))
                for c in coords:
                    self.assertEqual(acc.getValue(c), gridFG)
                for value in grid.iterOnValues():
                    self.assertTrue(value.min in coords)


    def testCopyToArray(self):
        import random
        import time

        
        try:
            import numpy as np
        except ImportError:
            return

        
        arr = np.zeros((1, 2, 1))
        grid = openvdb.FloatGrid()
        try:
            grid.copyFromArray(arr)
        except NotImplementedError:
            return

        
        grid = openvdb.FloatGrid()
        self.assertRaises(TypeError, lambda: grid.copyToArray('abc'))
        arr = np.zeros((1, 2))
        self.assertRaises(ValueError, lambda: grid.copyToArray(arr))

        
        arr = np.zeros((1, 2, 1), dtype = complex)
        grid = openvdb.FloatGrid()
        self.assertRaises(TypeError, lambda: grid.copyToArray(arr))

        ARRAY_DIM = 201
        BG, FG = 0, 1

        
        random.seed(0)
        def randCoord():
            return tuple(random.randint(0, ARRAY_DIM-1) for i in range(3))
        coords = set(randCoord() for i in range(200))

        def createArrays():
            
            for shape in (
                (ARRAY_DIM, ARRAY_DIM, ARRAY_DIM),      
                (ARRAY_DIM, ARRAY_DIM, ARRAY_DIM, 3)    
            ):
                for dtype in (np.float32, np.int32, np.float64, np.int64, np.uint32, np.bool):
                    
                    arr = np.ndarray(shape, dtype)
                    arr.fill(-100)
                    yield arr

        
        for cls in openvdb.GridTypes:
            
            if cls.valueTypeName.startswith('ptdataidx'):
                continue
            for arr in createArrays():
                isScalarArray = (len(arr.shape) == 3)
                isScalarGrid = False
                try:
                    len(cls.zeroValue) 
                except TypeError:
                    isScalarGrid = True 

                gridBG = valueFactory(cls.zeroValue, BG)
                gridFG = valueFactory(cls.zeroValue, FG)

                
                
                grid = cls(gridBG)
                acc = grid.getAccessor()
                for c in coords:
                    acc.setValueOn(c, gridFG)

                
                
                if isScalarGrid != isScalarArray:
                    self.assertRaises(ValueError, lambda: grid.copyToArray(arr))
                    continue

                
                
                grid.copyToArray(arr)
                
                
                
                

                
                for c in coords:
                    self.assertEqual(arr[c] if isScalarArray else tuple(arr[c]), gridFG)
                    arr[c] = gridBG
                self.assertEqual(np.amin(arr), BG)
                self.assertEqual(np.amax(arr), BG)


    def testMeshConversion(self):
        import time

        
        try:
            import numpy as np
        except ImportError:
            return

        

        
        cubeVertices = [(x, y, z) for x in (0, 100) for y in (0, 100) for z in (0, 100)]
        cubePoints = np.array(cubeVertices, float)

        
        cubeQuads = np.array([
            (0, 1, 3, 2), 
            (0, 2, 6, 4), 
            (4, 6, 7, 5), 
            (5, 7, 3, 1), 
            (2, 3, 7, 6), 
            (0, 4, 5, 1), 
        ], float)

        voxelSize = 2.0
        halfWidth = 3.0
        xform = openvdb.createLinearTransform(voxelSize)

        
        
        grids = []
        for gridType in [n for n in openvdb.GridTypes
            if n.__name__ in ('FloatGrid', 'DoubleGrid')]:

            
            try:
                grid = gridType.createLevelSetFromPolygons(
                    cubePoints, quads=cubeQuads, transform=xform, halfWidth=halfWidth)
            except NotImplementedError:
                return

            

            self.assertEqual(grid.transform, xform)
            self.assertEqual(grid.background, halfWidth * voxelSize)

            dim = grid.evalActiveVoxelDim()
            self.assertTrue(50 < dim[0] < 58)
            self.assertTrue(50 < dim[1] < 58)
            self.assertTrue(50 < dim[2] < 58)

            grids.append(grid)

        
        self.assertRaises(TypeError, lambda: openvdb.BoolGrid.createLevelSetFromPolygons(
            cubePoints, quads=cubeQuads, transform=xform, halfWidth=halfWidth))
        
        self.assertRaises(TypeError, lambda: openvdb.Vec3SGrid.createLevelSetFromPolygons(
            cubePoints, quads=cubeQuads, transform=xform, halfWidth=halfWidth))
        "points" argument to createLevelSetFromPolygons() must be a NumPy array.
        self.assertRaises(TypeError, lambda: openvdb.FloatGrid.createLevelSetFromPolygons(
            cubeVertices, quads=cubeQuads, transform=xform, halfWidth=halfWidth))
        "points" argument to createLevelSetFromPolygons() must be a NumPy float or int array.
        self.assertRaises(TypeError, lambda: openvdb.FloatGrid.createLevelSetFromPolygons(
            np.array(cubeVertices, bool), quads=cubeQuads, transform=xform, halfWidth=halfWidth))
        "triangles" argument to createLevelSetFromPolygons() must be an N x 3 NumPy array.
        self.assertRaises(TypeError, lambda: openvdb.FloatGrid.createLevelSetFromPolygons(
            cubePoints, triangles=cubeQuads, transform=xform, halfWidth=halfWidth))

        

        
        self.assertRaises(TypeError, lambda: openvdb.Vec3SGrid().convertToQuads())

        for grid in grids:
            points, quads = grid.convertToQuads()

            
            
            self.assertTrue(len(points) > 8)
            self.assertTrue(len(quads) > 6)
            pmin, pmax = points.min(0), points.max(0)
            self.assertTrue(-2 < pmin[0] < 2)
            self.assertTrue(-2 < pmin[1] < 2)
            self.assertTrue(-2 < pmin[2] < 2)
            self.assertTrue(98 < pmax[0] < 102)
            self.assertTrue(98 < pmax[1] < 102)
            self.assertTrue(98 < pmax[2] < 102)

            points, triangles, quads = grid.convertToPolygons(adaptivity=1)

            self.assertTrue(len(points) > 8)
            pmin, pmax = points.min(0), points.max(0)
            self.assertTrue(-2 < pmin[0] < 2)
            self.assertTrue(-2 < pmin[1] < 2)
            self.assertTrue(-2 < pmin[2] < 2)
            self.assertTrue(98 < pmax[0] < 102)
            self.assertTrue(98 < pmax[1] < 102)
            self.assertTrue(98 < pmax[2] < 102)


if __name__ == '__main__':
    print('Testing %s' % os.path.dirname(openvdb.__file__))
    sys.stdout.flush()

    args = sys.argv

    "-t" flag to identify test names,
    "-t" arguments,
    "TestOpenVDB.py -t TestOpenVDB.testTransform"
    "TestOpenVDB.py TestOpenVDB.testTransform".
    args = [a for a in args if a != '-t']

    unittest.main(argv=args)

