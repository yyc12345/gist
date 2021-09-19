using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Numerics;

namespace EquationBalance {
    class Program {

        static string[] elements = {
            "H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K",
            "Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
            "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm",
            "Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb",
            "Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",
            "Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"
        };
        static string getElements(int id) {
            return elements[id];
        }

        static void Main(string[] args) {

            var data = ReadTree(args[0]);
            foreach (var item in data) {
                Console.WriteLine(item.showcase);
                var mat = GetEquationMatrix(item);
                SolveMatrix(mat);
            }

            Console.ReadKey();

        }


        static EquationTreeNode[] ReadTree(string filename) {
            var fs = new FileStream(filename, FileMode.Open, FileAccess.Read, FileShare.Read);
            var br = new BinaryReader(fs);

            Stack<EquationTreeNode> nodeStack = new Stack<EquationTreeNode>();
            IndexDistrubtor distributor = new IndexDistrubtor();
            while (br.BaseStream.Position != br.BaseStream.Length) {
                var node = new EquationTreeNode();
                node.type = (EquationTreeNodeType)br.ReadInt32();
                node.ruleId = br.ReadInt32();
                node._nodeId = distributor.Next();
                node.elements = new Dictionary<int, int>();

                switch (node.type) {
                    case EquationTreeNodeType.Atom: {
                            node.children = null;

                            switch (node.ruleId) {
                                case 1:
                                    node.extraProp = new int[1];
                                    node.extraProp[0] = br.ReadInt32();
                                    node.elements.Add(node.extraProp[0], 1);
                                    node.showcase = getElements(node.extraProp[0]);
                                    break;
                                case 2:
                                    node.extraProp = new int[2];
                                    node.extraProp[0] = br.ReadInt32();
                                    node.extraProp[1] = br.ReadInt32();
                                    node.elements.Add(node.extraProp[0], node.extraProp[1]);
                                    node.showcase = $"{getElements(node.extraProp[0])}{node.extraProp[1].ToString()}";
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.BracketAtomGroup: {
                            node.children = new EquationTreeNode[1];
                            node.children[0] = nodeStack.Pop();

                            switch (node.ruleId) {
                                case 1:
                                    node.extraProp = null;
                                    node.elements = node.children[0].elements.DictMerge(null);
                                    node.showcase = '(' + node.children[0].showcase + ')';
                                    break;
                                case 2:
                                    node.extraProp = new int[1];
                                    node.extraProp[0] = br.ReadInt32();
                                    node.elements = node.children[0].elements.DictMultiply(node.extraProp[0]);
                                    node.showcase = '(' + node.children[0].showcase + ')' + node.extraProp[0].ToString();
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.AtomGroup: {
                            node.extraProp = null;

                            switch (node.ruleId) {
                                case 1:
                                case 2:
                                    node.children = new EquationTreeNode[1];
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = node.children[0].elements.DictMerge(null);
                                    node.showcase = node.children[0].showcase;
                                    break;
                                case 3:
                                case 4:
                                    node.children = new EquationTreeNode[2];
                                    node.children[1] = nodeStack.Pop();
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = node.children[0].elements.DictMerge(node.children[1].elements);
                                    node.showcase = node.children[0].showcase + node.children[1].showcase;
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.IntervalPart: {
                            node.children = new EquationTreeNode[1];
                            node.children[0] = nodeStack.Pop();

                            switch (node.ruleId) {
                                case 1:
                                    node.extraProp = null;
                                    node.elements = node.children[0].elements.DictMerge(null);
                                    node.showcase = node.children[0].showcase;
                                    break;
                                case 2:
                                    node.extraProp = new int[1];
                                    node.extraProp[0] = br.ReadInt32();
                                    node.elements = node.children[0].elements.DictMultiply(node.extraProp[0]);
                                    node.showcase = node.extraProp[0].ToString() + node.children[0].showcase;
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.EquationPart: {
                            node.extraProp = null;

                            switch (node.ruleId) {
                                case 1:
                                    node.children = new EquationTreeNode[1];
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = node.children[0].elements.DictMerge(null);
                                    node.showcase = node.children[0].showcase;
                                    break;
                                case 2:
                                    node.children = new EquationTreeNode[2];
                                    node.children[1] = nodeStack.Pop();
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = node.children[0].elements.DictMerge(node.children[1].elements);
                                    node.showcase = node.children[0].showcase + '·' + node.children[1].showcase;
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.EquationSide: {
                            node.extraProp = null;

                            switch (node.ruleId) {
                                case 1:
                                    node.children = new EquationTreeNode[1];
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = null;   // don't need this for the level of node above EquationPart
                                    node.showcase = node.children[0].showcase;
                                    break;
                                case 2:
                                    node.children = new EquationTreeNode[2];
                                    node.children[1] = nodeStack.Pop();
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = null;   // don't need this for the level of node above EquationPart
                                    node.showcase = node.children[0].showcase + '+' + node.children[1].showcase;
                                    break;
                            }
                        }
                        break;
                    case EquationTreeNodeType.Equation: {
                            node.extraProp = null;

                            switch (node.ruleId) {
                                case 1:
                                    node.children = null;
                                    node.elements = null;
                                    node.showcase = null;
                                    // ignore blank equation
                                    break;
                                case 2:
                                    node.children = new EquationTreeNode[2];
                                    node.children[1] = nodeStack.Pop();
                                    node.children[0] = nodeStack.Pop();
                                    node.elements = null;   // don't need this for the level of node above EquationPart
                                    node.showcase = node.children[0].showcase + '=' + node.children[1].showcase;
                                    break;
                            }
                        }
                        break;
                }

                nodeStack.Push(node);
            }

            br.Close();
            br.Dispose();
            fs.Dispose();

            var ls = new List<EquationTreeNode>();
            while (nodeStack.Count != 0) {
                var node = nodeStack.Pop();
                if (node.type == EquationTreeNodeType.Equation &&
                    node.ruleId == 1) {
                    ; // drop blank equation
                } else
                    ls.Add(node);
            }
            ls.Reverse();
            return ls.ToArray();
        }

        static Matrix GetEquationMatrix(EquationTreeNode root) {
            // get each item's elements dict
            var stack = new Stack<TreeNodeWithStage>();
            var sheet = new List<Dictionary<int, int>>();

            stack.Push(new TreeNodeWithStage(root));
            bool isLeft = true;
            while (stack.Count != 0) {
                var inode = stack.Peek();

                switch (inode.node.type) {
                    case EquationTreeNodeType.Atom:
                    case EquationTreeNodeType.BracketAtomGroup:
                    case EquationTreeNodeType.AtomGroup:
                    case EquationTreeNodeType.IntervalPart:
                    case EquationTreeNodeType.EquationPart:
                        sheet.Add(inode.node.elements.DictMultiply(isLeft ? 1 : -1));
                        break;
                    case EquationTreeNodeType.EquationSide:
                        if (inode.stage == 1) {
                            foreach (var item in inode.node.children)
                                stack.Push(new TreeNodeWithStage(item));
                            inode.stage++;
                            continue;
                        }
                        break;
                    case EquationTreeNodeType.Equation:
                        if (inode.stage == 1) {
                            stack.Push(new TreeNodeWithStage(inode.node.children[0]));
                            inode.stage++;
                            continue;
                        } else if (inode.stage == 2) {
                            isLeft = false;
                            stack.Push(new TreeNodeWithStage(inode.node.children[1]));
                            inode.stage++;
                            continue;
                        }
                        break;
                }

                stack.Pop();
            }

            // make dict as matrix
            int distributor = 0;
            Dictionary<int, int> distributorReflect = new Dictionary<int, int>();
            int eles;
            foreach (var item in sheet) {
                foreach (var key in item.Keys) {
                    if (!distributorReflect.TryGetValue(key, out eles)) {
                        //add new reflect
                        distributorReflect.Add(key, distributor);
                        distributor++;
                    }
                }
            }
            var mat = new Matrix(distributorReflect.Count, sheet.Count);
            int r;
            for (int c = 0; c < sheet.Count; c++) {
                foreach (var pair in sheet[c]) {
                    r = distributorReflect[pair.Key];
                    mat.eles[r][c] = pair.Value;
                }
            }

#if DEBUG
            var debug_elements = new string[distributorReflect.Count];
            foreach (var pair in distributorReflect) {
                debug_elements[pair.Value] = getElements(pair.Key);
            }

            for (int _r = 0; _r < mat.rows; _r++) {
                Console.Write(debug_elements[_r]);
                Console.Write("\t");
                for (int _c = 0; _c < mat.columns; _c++) {
                    Console.Write(mat.eles[_r][_c]);
                    Console.Write("\t");
                }
                Console.Write("\n");
            }
            Console.Write("\n");
#endif

            return mat;
        }

        static BigInteger[][] SolveMatrix(Matrix mat) {
            // transform matrix
            int p_row = 0;
            int p_col = 0;

            while (p_row < mat.rows && p_col < mat.columns) {
                if (mat.is_blank(p_col, p_row)) {
                    p_col++;
                    continue;
                    // all of this column is zero, skip this and go to next column
                }
                if (mat.eles[p_row][p_col] == 0) {
                    // but current row is start with zero, we need swap it with a non-zero start row
                    mat.swap(p_row, mat.pick_nozero(p_col, p_row));
                }

                // get lcm
                if (mat.eles[p_row][p_col].Sign < 0) mat.reverse_row(p_row);
                var lcm = mat.lcm_column(p_col, p_row);
                var div = lcm / mat.eles[p_row][p_col];
                for (int r = p_row + 1; r < mat.rows; r++) {
                    if (mat.eles[r][p_col].IsZero) continue; // skip zero start row

                    var divt = lcm / mat.eles[r][p_col];
                    if (divt.Sign < 0) divt = -divt;

                    mat.add2(p_col, p_row, div, r, divt,
                        mat.eles[r][p_col].Sign > 0
                    );
                }

                // gcd current line
                mat.gcd_row(p_row);

                // process next;
                p_col++;
                p_row++;
            }

#if DEBUG
            for (int _r = 0; _r < mat.rows; _r++) {
                Console.Write("\t");
                for (int _c = 0; _c < mat.columns; _c++) {
                    Console.Write(mat.eles[_r][_c]);
                    Console.Write("\t");
                }
                Console.Write("\n");
            }
            Console.Write("\n");
#endif

            // try solve transformed matrix
            // get solution count
            var x_count = mat.columns - mat.rank();
            if (x_count <= 0) {
                // only zero solution or no solution
                return null;
            }

            // pick free variable
            int[] free_var_index = new int[x_count];
            int[] pending_index = new int[mat.columns - x_count];
            int pointer_fvi = 0;
            int pointer_pending = 0;
            int top = -1;
            for (int c = 0; c < mat.columns; c++) {
                for (int r = mat.rows - 1; r >= 0; r--) {
                    if (!mat.eles[r][c].IsZero) {
                        // non-zero, mark it
                        if (top == r) {
                            // not the first non-zero item, use it, and goto next col
                            free_var_index[pointer_fvi] = c;
                            pointer_fvi++;
                        } else {
                            // no, update top
                            // add this column to pending index
                            pending_index[pointer_pending] = c;
                            pointer_pending++;
                            top = r;
                        }
                        break;
                    }
                }
            }

            //construct each fundemental solution
            var result = new BigInteger[x_count][];
            for (int x = 0; x < x_count; x++) {
                result[x] = new BigInteger[mat.columns];
                for (int ix = 0; ix < mat.columns; ix++) {
                    result[x][ix] = 0;
                }
            }

            for (int xid = 0; xid < x_count; xid++) {
                // set pending pointer
                pointer_pending = pending_index.Length - 1;
                // write current free variable
                result[xid][free_var_index[xid]] = 1;
                for (int r = mat.rows - 1; r >= 0; r--) {
                    // get sum of all item in current row
                    BigInteger num = 0, deno = 0;
                    for (int c = 0; c < mat.columns; c++) {
                        if (c == pending_index[pointer_pending]) {
                            deno = -mat.eles[r][c];
                        } else if (!result[xid][c].IsZero) {
                            num = num + result[xid][c] * mat.eles[r][c];
                        }
                    }

                    if (deno.Sign < 0) {
                        deno = -deno;
                        num = -num;
                    }

                    // write data
                    // and gcd existed item
                    BigInteger gcd = 0;
                    result[xid][pending_index[pointer_pending]] = num;
                    for (int c = 0; c < mat.columns; c++) {
                        if (c == pending_index[pointer_pending]) {
                            result[xid][c] = num;
                            gcd = Utils.gcd(gcd, num);
                        } else if (!result[xid][c].IsZero) {
                            result[xid][c] = result[xid][c] * deno;
                            gcd = Utils.gcd(gcd, result[xid][c]);
                        }
                    }
                    for (int c = 0; c < mat.columns; c++) {
                        if (!result[xid][c].IsZero) {
                            result[xid][c] /= gcd;
                        }
                    }

                    pointer_pending--;
                }
            }


#if DEBUG
            for (int _r = 0; _r < x_count; _r++) {
                for (int _c = 0; _c < mat.columns; _c++) {
                    Console.Write(result[_r][_c]);
                    Console.Write("\t");
                }
                Console.Write("\n");
            }
            Console.Write("\n");
#endif

            return result;
        }
    }

    public static class Utils {
        public static Dictionary<int, int> DictMerge(this Dictionary<int, int> _dict1, Dictionary<int, int> dict2) {
            var dict1 = new Dictionary<int, int>(_dict1);

            if (dict2 == null) return dict1;

            int ov;
            foreach (var pair in dict2) {
                if (dict1.TryGetValue(pair.Key, out ov)) {
                    // have key, add them
                    dict1[pair.Key] = ov + pair.Value;
                } else {
                    dict1.Add(pair.Key, pair.Value);
                }
            }

            return dict1;
        }

        public static Dictionary<int, int> DictMultiply(this Dictionary<int, int> _dict, int num) {
            var dict = new Dictionary<int, int>();
            foreach (var pair in _dict) {
                dict[pair.Key] = num * pair.Value;
            }
            return dict;
        }

        public static BigInteger gcd(BigInteger x, BigInteger y) {
            if (x.Sign < 0) x = -x;
            if (y.Sign < 0) y = -y;

            BigInteger cache;
            if (x < y) {
                cache = x;
                x = y;
                y = cache;
            }

            while (y != 0) {
                cache = x % y;
                x = y;
                y = cache;
            }
            return x;
        }

        public static BigInteger lcm(BigInteger x, BigInteger y) {
            if (x.Sign < 0) x = -x;
            if (y.Sign < 0) y = -y;

            return x / gcd(x, y) * y;
        }
    }

    enum EquationTreeNodeType : int {
        Atom = 1,
        BracketAtomGroup = 2,
        AtomGroup = 3,
        IntervalPart = 4,
        EquationPart = 5,
        EquationSide = 6,
        Equation = 7
    }

    class TreeNodeWithStage {
        public TreeNodeWithStage(EquationTreeNode node) {
            this.node = node;
            stage = 1;
        }
        public EquationTreeNode node;
        public int stage;
    }

    class EquationTreeNode {
        public EquationTreeNodeType type;
        public int ruleId;
        public int[] extraProp;
        public EquationTreeNode[] children;
        public Dictionary<int, int> elements;
        public string showcase;

        public int _nodeId;
    }

    class IndexDistrubtor {
        public IndexDistrubtor() {
            id = 0;
        }
        int id;
        public int Next() {
            return id++;
        }
    }

    class Matrix {
        public Matrix(int rows, int columns) {
            this.rows = rows;
            this.columns = columns;
            eles = new BigInteger[rows][];
            for (int i = 0; i < rows; i++) {
                eles[i] = new BigInteger[columns];
                for (int j = 0; j < columns; j++) {
                    eles[i][j] = 0;
                }
            }
        }
        public BigInteger[][] eles;
        public int rows;
        public int columns;

        public void swap(int row1, int row2) {
            var swap = eles[row1];
            eles[row1] = eles[row2];
            eles[row2] = swap;
        }

        public void add2(int start_col, int row, BigInteger num, int row_target, BigInteger num_target, bool is_minus) {
            for (int c = start_col; c < columns; c++) {
                eles[row_target][c] *= num_target;
                if (is_minus) eles[row_target][c] -= eles[row][c] * num;
                else eles[row_target][c] += eles[row][c] * num;
            }
        }

        public void reverse_row(int row) {
            for (int c = 0; c < columns; c++) {
                if (eles[row][c].Sign != 0) eles[row][c] = -eles[row][c];
            }
        }

        public bool is_blank(int col, int start_row) {
            for (int r = start_row; r < rows; r++) {
                if (eles[r][col] != 0) return false;
            }
            return true;
        }

        public BigInteger lcm_column(int col, int start_row) {
            BigInteger v = 1;
            for (int r = start_row; r < rows; r++) {
                if (eles[r][col] != 0) v = Utils.lcm(v, eles[r][col]);
            }
            return v;
        }

        public void gcd_row(int row) {
            BigInteger v = 1;
            bool is_non_zero = false;
            for (int c = 0; c < columns; c++) {
                if (eles[row][c] != 0) {
                    if (is_non_zero) {
                        v = Utils.gcd(v, eles[row][c]);
                    } else {
                        v = eles[row][c];
                        is_non_zero = true;
                    }
                }
            }

            if (!is_non_zero) return;

            for (int c = 0; c < columns; c++) {
                eles[row][c] /= v;
            }
        }

        public int pick_nozero(int col, int start_row) {
            for (int r = start_row; r < rows; r++) {
                if (eles[r][col] != 0) return r;
            }
            return start_row;
        }

        public int rank() {
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = 0; c < columns; c++) {
                    if (eles[r][c] != 0) return r + 1;
                }
            }
            return 0;
        }

    }

}
