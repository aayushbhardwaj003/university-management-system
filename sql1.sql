CREATE DATABASE college;
drop database college;
USE college;


CREATE TABLE student (
rollno INT PRIMARY KEY,
name VARCHAR(50),
marks INT NOT NULL,
grade VARCHAR(1),
city VARCHAR(20)
);

INSERT INTO student
(rollno, name, marks, grade, city)
VALUES
(101, "anil", 78, "C", "Pune"),
(102, "bhumika", 93, "A", "Mumbai"), 
(103, "chetan", 85, "B", "Mumbai"), 
(104, "dhruv", 96, "A", "Delhi"), 
(105, "emanuel", 12, "F", "Delhi"),
(106, "farah", 82, "B", "Delhi");

alter table student
add coluTablesmn branch varchar(20);

update student
set rollno=111
where rollno=101;

select * from student;

select city, COUNT(rollno) as rollno
from student
group by city;

select count(marks),grade
from student
group by grade
having grade>'C';


select count(rollno),city
from student
group by city
having max(marks)>80;

SELECT city,count(*)
FROM student
where marks>=60
GROUP BY city
HAVING count(*)>=2
ORDER BY city ASC;

alter table student
add column age int not null default 20;

alter table student
drop column age;

alter table student
modify column age varchar(2);

insert into student
(rollno, name, marks, stu_age)
values
(111, "Ritu", 82, 121);

alter table student
change name full_name varchar(30);

alter table stu
rename to student;

select * from student;

truncate table student;

delete from student
where grade="F";

alter table student
drop column grade;



-- ------------------------teacher & dept table------------------;

CREATE TABLE dept (
id int primary key,
name varchar(30)
);

CREATE TABLE teacher (
id int primary key,
name varchar(30),
dept_id int,
foreign key (dept_id) references dept(id)
on update cascade
on delete cascade
);

insert into dept
values
(101, "economics"),
(102, "IT");

update dept
set id=111
where id=101;

insert into teacher
values
(1, "Ram", 101),
(2,"Rakesh",102);

select * from teacher;

-- ---------------joins--------------------------

create table stud(
	rollno int primary key,
    name varchar(30),
    city varchar(20)
);

insert into stud
values
(1,"AAyush","patna"),
(2,"satya","Puri"),
(3,"aakash","dbg"),
(4,"wefe","bbs"),
(5,"ryh","spj")

;

select * from stud;


create table teac(
	id int primary key,
    name varchar(30),
    city varchar(20)
);

insert into teac
values
(443,"rgergg","ssns");
-- (101,"anupam","patna"),
-- (202,"rishabh","Puri"),
-- (303,"sffd","dbg"),
-- (3,"rfrf","dbg");

truncate table stud;
truncate table teac;

select * from teac;

select *
from stud
inner join teac
on stud.city=teac.city;

select *
from stud
left join teac
on stud.city=teac.city;

-- fulll join
select *
from stud
left join teac
on stud.city=teac.city
union
select *
from stud
right join teac
on stud.city=teac.city
;

-- left exclusion join
select *
from stud
left join teac
on stud.city=teac.city
where teac.city is null;

-- right exclusion join
select *
from stud
right join teac
on stud.city=teac.city
where stud.city is null;

-- full exclusive join
select *
from stud
left join teac
on stud.city=teac.city
where teac.city is null
union
select *
from stud
right join teac
on stud.city=teac.city
where stud.city is null;

CREATE TABLE Employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT
);

INSERT INTO Employee 
(id, name, manager_id)
VALUES 
(101, 'adam', 103),
(102, 'bob', 104),
(103, 'casey', NULL),
(104, 'donald', 103);

select * from employee;

-- self join
select b.name, a.name as manager_name
from employee as a
join employee as b
on a.id=b.manager_id;

-- union
select name from employee
union 
select full_name from student;

alter table stud
change name stu_name varchar(30);

alter table teac
change name teac_name varchar(30);