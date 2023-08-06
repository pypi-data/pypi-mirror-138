"""Python Counter for counting different parts of a program."""

import libcst.matchers as m
import libcst as cst


class PyPiCount:
    """Class for the python counter."""

    def __init__(self, filename):
        """Declaring the self variable."""
        with open(filename, 'r', encoding="utf8") as file:
            self.search = cst.parse_module(file.read())

    def count_class_definitions(self):
        """Counting the class definitions."""
        return len(m.findall(self.search, m.ClassDef()))


    def count_comments(self):
        """Counting the comments."""
        return len(m.findall(self.search, m.Comment()))


    def count_import_statements(self):
        """Counting the import statements."""
        return len(m.findall(self.search, m.Import()))


    def count_if_statements(self):
        """Counting the if statements."""
        return len(m.findall(self.search, m.If()))

    def count_while_loops(self):
        """Counting the while loops."""
        return len(m.findall(self.search, m.While()))

    def count_for_loops(self):
        """Counting the for loops."""
        return len(m.findall(self.search, m.For()))

    def count_function_definitions(self):
        """Counting the function definitions."""
        func_definitions = m.findall(self.search, m.FunctionDef())
        return len(func_definitions)


    def count_functions_without_docstrings(self):  # pylint: disable=R1710
        """Counting the function definitions without docstrings."""
        functions_list = m.findall(self.search, m.FunctionDef())
        count = 0
        total_count = []
        for find in functions_list:
            if find.get_docstring() is None:
                total_count.append(count)
                count += 1
        return count


    def count_functions_with_docstrings(self):  # pylint: disable=R1710
        """Counting the function definitions with docstrings."""
        function_definitions2 = m.findall(self.search, m.FunctionDef())
        count = 0
        total = []
        for finding in function_definitions2:
            if finding.get_docstring() is not None:
                count += 1
                total.append(count)
        return count

    def count_classes_without_docstrings(self):  # pylint: disable=R1710
        """Counting the class definitions without docstrings."""
        class_definitions = m.findall(self.search, m.ClassDef())
        count = 0
        total_count = []
        for find in class_definitions:
            if find.get_docstring() is None:
                total_count.append(count)
                count += 1
        return count


    def count_classes_with_docstrings(self):  # pylint: disable=R1710
        """Counting the class definitions without docstrings."""
        class_definitions2 = m.findall(self.search, m.ClassDef())
        count = 0
        total = []
        for find in class_definitions2:
            if find.get_docstring() is not None:
                total.append(count)
                count += 1
        return count

    def count_function_parameters(self, function_name):
        """Counting the parameters within a function."""
        functions = m.findall(self.search, m.FunctionDef())
        param_result = 0
        for func in functions:
            if func.name.value == function_name:
                param_result = len(func.params.params)
        return param_result

    def count_assignment_statements(self):
        """Counting the assignment statement."""
        assignment_statement = m.findall(self.search, m.Assign())
        return len(assignment_statement)

    def count_augmented_assignment_statements(self):
        """Counting the augmented assignment statement."""
        aug_assignment_statement = m.findall(self.search, m.AugAssign())
        return len(aug_assignment_statement)
