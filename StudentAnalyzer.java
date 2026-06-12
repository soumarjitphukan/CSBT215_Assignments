import java.util.*;
import java.util.stream.*;

class Student {
    int id;
    String name;
    List<String> courses;
    Map<String, Integer> scores;

    Student(int id, String name, List<String> courses, Map<String, Integer> scores) {
        this.id = id;
        this.name = name;
        this.courses = courses;
        this.scores = scores;
    }

    double getAverageScore() {
        return scores.values()
                .stream()
                .mapToInt(Integer::intValue)
                .average()
                .orElse(0.0);
    }
}

class StudentAnalyzer {

    public static List<Student> getTopNStudents(List<Student> students, int n) {
        return students.stream()
                .sorted(Comparator.comparingDouble(Student::getAverageScore).reversed())
                .limit(n)
                .collect(Collectors.toList());
    }

    public static Map<String, Double> getAverageScorePerCourse(List<Student> students) {

        Map<String, List<Integer>> courseScores = new HashMap<>();

        students.forEach(student ->
                student.courses.forEach(course ->
                        courseScores
                                .computeIfAbsent(course, k -> new ArrayList<>())
                                .add(student.scores.getOrDefault(course, 0))
                )
        );

        return courseScores.entrySet()
                .stream()
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        e -> e.getValue()
                                .stream()
                                .mapToInt(Integer::intValue)
                                .average()
                                .orElse(0.0)
                ));
    }

    public static Set<String> getAllUniqueCourses(List<Student> students) {
        return students.stream()
                .flatMap(s -> s.courses.stream())
                .collect(Collectors.toCollection(HashSet::new));
    }

    public static void main(String[] args) {

        List<Student> students = new ArrayList<>();

        Map<String, Integer> scores1 = new HashMap<>();
        scores1.put("Math", 85);
        scores1.put("Physics", 90);

        Map<String, Integer> scores2 = new HashMap<>();
        scores2.put("Math", 78);
        scores2.put("Chemistry", 88);

        Map<String, Integer> scores3 = new HashMap<>();
        scores3.put("Physics", 92);
        scores3.put("Chemistry", 80);

        students.add(new Student(1, "Alice",
                Arrays.asList("Math", "Physics"), scores1));

        students.add(new Student(2, "Bob",
                Arrays.asList("Math", "Chemistry"), scores2));

        students.add(new Student(3, "Charlie",
                Arrays.asList("Physics", "Chemistry"), scores3));

        System.out.println(getTopNStudents(students, 2)
                .stream()
                .map(s -> s.name)
                .collect(Collectors.toList()));

        System.out.println(getAverageScorePerCourse(students));

        System.out.println(getAllUniqueCourses(students));
    }
}

/*
Time Complexity:

Computing course averages:
O(n * c)
n = number of students
c = courses per student

Sorting top N students:
O(n log n)

Space Complexity:

Course score storage: O(k + n*c)
k = number of unique courses
*/