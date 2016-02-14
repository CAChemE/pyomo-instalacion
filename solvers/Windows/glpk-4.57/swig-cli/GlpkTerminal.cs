using System;
using System.Collections.Generic;

namespace org.gnu.glpk {

    /**
     * This class manages callbacks from the MIP solver.
     * <p>The GLPK MIP solver calls method {@link #callback(IntPtr) callback} in
     * the branch-and-cut algorithm. A listener to the callback can be used to
     * influence the sequence in which nodes of the search tree are evaluated,
     * or to supply a heuristic solution. To find out why the callback is
     * issued use method {@link GLPK#glp_ios_reason(glp_tree)
     * GLPK.glp_ios_reason}.
     */
    public class GlpkTerminal {

        /**
         * List of callback listeners.
         */
        private static LinkedList<IGlpkTerminalListener> listeners
                = new LinkedList<IGlpkTerminalListener>();

        /**
         * Constructor.
         */
        private GlpkTerminal() {
        }

        /**
         * Callback function called by native library.
         * Output to the console is created if any of the listeners requests it.
         * @param str string to be written to console
         * @return 0 if output is requested
         */
        public static int callback(string str) {
            bool output = false;

            if (listeners.Count > 0) {
                foreach (IGlpkTerminalListener listener in listeners) {
                    output |= listener.output(str);
                }
                if (output) {
                    return 0;
                } else {
                    return 1;
                }
            }
            return 0;
        }
        
        /**
         * Adds a listener for callbacks.
         * @param listener listener for callbacks
         */
        public static void addListener(IGlpkTerminalListener listener) {
            GLPK.glp_term_hook(null, null);
            listeners.AddLast(listener);
        }

        /**
         * Removes first occurance of a listener for callbacks.
         * @param listener listener for callbacks
         * @return true if the listener was found
         */
        public static bool removeListener(IGlpkTerminalListener listener) {
            if (listeners.Contains(listener)) {
                listeners.Remove(listener);
                return true;
            } else {
                return false;
            }
        }
    }
}
