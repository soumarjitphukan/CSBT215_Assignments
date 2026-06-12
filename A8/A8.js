import React, { useState } from "react";

export default function EnrollmentDashboard() {

  const [studentsMap, setStudentsMap] = useState(new Map());

  const addStudent = (student) => {
    const newMap = new Map(studentsMap);
    newMap.set(student.id, student);
    setStudentsMap(newMap);
  };

  const removeStudent = (id) => {
    const newMap = new Map(studentsMap);
    newMap.delete(id);
    setStudentsMap(newMap);
  };

  const studentsArray = [...studentsMap.values()];

  const sortedStudents = [...studentsArray].sort((a, b) => b.gpa - a.gpa);

  const uniqueCourses = Array.from(
    studentsArray.reduce((set, s) => {
      s.enrolledCourses.forEach(c => set.add(c));
      return set;
    }, new Set())
  );

  const filterByCourse = (course) =>
    studentsArray.filter(s => s.enrolledCourses.has(course));

  return (
    <div>
      <h2>Students</h2>

      <button
        onClick={() =>
          addStudent({
            id: Date.now(),
            name: "New Student",
            enrolledCourses: new Set(["Math"]),
            gpa: Math.random() * 4
          })
        }
      >
        Add Student
      </button>

      <h3>Sorted by GPA</h3>
      <ul>
        {sortedStudents.map(s => (
          <li key={s.id}>
            {s.name} - GPA: {s.gpa.toFixed(2)}
            <button onClick={() => removeStudent(s.id)}>Remove</button>
          </li>
        ))}
      </ul>

      <h3>Unique Courses</h3>
      <ul>
        {uniqueCourses.map(c => (
          <li key={c}>{c}</li>
        ))}
      </ul>

      <h3>Students in Math</h3>
      <ul>
        {filterByCourse("Math").map(s => (
          <li key={s.id}>{s.name}</li>
        ))}
      </ul>
    </div>
  );
}

/*
Time Complexity:

Filtering students by course:
O(n)

n = number of students
Each student membership check in Set = O(1)

Total complexity = O(n)

Space Complexity:
O(n + c)

n = number of students
c = number of unique courses
*/