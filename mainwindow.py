<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>901</width>
    <height>424</height>
   </rect>
  </property>
  <property name="maximumSize">
   <size>
    <width>1920</width>
    <height>1080</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(0, 0, 0);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout_12">
    <item row="0" column="1">
     <widget class="QFrame" name="frame_10">
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_10">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_3">
         <item>
          <widget class="QLabel" name="label_arrow_up">
           <property name="text">
            <string>ArrUp</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_grade_move_pos">
           <property name="styleSheet">
            <string notr="true">color: rgb(51, 255, 0);</string>
           </property>
           <property name="text">
            <string>-0.1</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_grade_move_neg">
           <property name="styleSheet">
            <string notr="true">color: rgb(224, 27, 36);</string>
           </property>
           <property name="text">
            <string>-0.1</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_arrow_down">
           <property name="styleSheet">
            <string notr="true"/>
           </property>
           <property name="text">
            <string>ArrDo</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="2" column="4">
     <widget class="QFrame" name="frame_9">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_9">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_10">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_12">
           <item>
            <spacer name="horizontalSpacer_16">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_courses_open_bottom_right">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
</string>
             </property>
             <property name="text">
              <string>Courses Open</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_17">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_13">
           <item>
            <spacer name="horizontalSpacer_15">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_courses_open_number_bottom_right">
             <property name="styleSheet">
              <string notr="true">font: 700 60pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>57</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_18">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="1" column="1" colspan="2">
     <widget class="QFrame" name="frame_5">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_3">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_12">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_5">
           <item>
            <spacer name="horizontalSpacer">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_course_status">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Course Status</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_2">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <widget class="QFrame" name="frame_pie_chart">
           <property name="frameShape">
            <enum>QFrame::Shape::StyledPanel</enum>
           </property>
           <property name="frameShadow">
            <enum>QFrame::Shadow::Raised</enum>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="0" column="3">
     <widget class="QFrame" name="frame_2">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_2">
       <item row="0" column="1">
        <layout class="QVBoxLayout" name="verticalLayout_6">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_6">
           <item>
            <spacer name="horizontalSpacer_3">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_best_streak">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
</string>
             </property>
             <property name="text">
              <string>Best: 7 Days</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_4">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_2">
           <item alignment="Qt::AlignmentFlag::AlignHCenter">
            <widget class="QLabel" name="label_current">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>Current</string>
             </property>
            </widget>
           </item>
           <item alignment="Qt::AlignmentFlag::AlignHCenter">
            <widget class="QLabel" name="label_current_streak_number">
             <property name="styleSheet">
              <string notr="true">font: 700 60pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>4</string>
             </property>
            </widget>
           </item>
           <item alignment="Qt::AlignmentFlag::AlignHCenter">
            <widget class="QLabel" name="label_streak">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>Streak</string>
             </property>
            </widget>
           </item>
          </layout>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="0" column="0" rowspan="3">
     <widget class="QFrame" name="frame_left_side">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QHBoxLayout" name="horizontalLayout">
       <item>
        <layout class="QVBoxLayout" name="verticalLayout_2">
         <item>
          <layout class="QVBoxLayout" name="verticalLayout">
           <item>
            <widget class="QLabel" name="label_student_name">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Name:</string>
             </property>
             <property name="textFormat">
              <enum>Qt::TextFormat::AutoText</enum>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QLabel" name="label_input_student_name">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>Bastian Schwab</string>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QLabel" name="label_student_number">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Student-Number:</string>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QLabel" name="label_input_student_number">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>IU14095471</string>
             </property>
            </widget>
           </item>
          </layout>
         </item>
         <item>
          <spacer name="verticalSpacer">
           <property name="orientation">
            <enum>Qt::Orientation::Vertical</enum>
           </property>
           <property name="sizeHint" stdset="0">
            <size>
             <width>175</width>
             <height>88</height>
            </size>
           </property>
          </spacer>
         </item>
         <item>
          <layout class="QFormLayout" name="formLayout">
           <item row="0" column="0">
            <widget class="QLabel" name="label_add_grade">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Add Grade</string>
             </property>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QPushButton" name="pushButton_add_grade">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>+</string>
             </property>
            </widget>
           </item>
           <item row="1" column="0">
            <widget class="QLabel" name="label_add_course">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Add Course</string>
             </property>
            </widget>
           </item>
           <item row="1" column="1">
            <widget class="QPushButton" name="pushButton_add_course">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>+</string>
             </property>
            </widget>
           </item>
           <item row="2" column="0">
            <widget class="QLabel" name="label_add_semester">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>Add Semester</string>
             </property>
            </widget>
           </item>
           <item row="2" column="1">
            <widget class="QPushButton" name="pushButton_add_semester">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>+</string>
             </property>
            </widget>
           </item>
          </layout>
         </item>
         <item>
          <spacer name="verticalSpacer_2">
           <property name="orientation">
            <enum>Qt::Orientation::Vertical</enum>
           </property>
           <property name="sizeHint" stdset="0">
            <size>
             <width>175</width>
             <height>88</height>
            </size>
           </property>
          </spacer>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="2" column="1" colspan="2">
     <widget class="QFrame" name="frame_4">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_7">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_8">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_9">
           <item>
            <spacer name="horizontalSpacer_9">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_semester_bottom_left">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
</string>
             </property>
             <property name="text">
              <string>Semester</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_10">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_8">
           <item>
            <spacer name="horizontalSpacer_7">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_semester_number_bottom_left">
             <property name="styleSheet">
              <string notr="true">font: 700 60pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>2</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_8">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="2" column="3">
     <widget class="QFrame" name="frame_8">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_8">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_9">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_10">
           <item>
            <spacer name="horizontalSpacer_14">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_courses_completet_bottom_mid">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
</string>
             </property>
             <property name="text">
              <string>Courses Completet</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_13">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_11">
           <item>
            <spacer name="horizontalSpacer_11">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_courses_completet_number_bottom_mid">
             <property name="styleSheet">
              <string notr="true">font: 700 60pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>5</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_12">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="1" column="3" colspan="2">
     <widget class="QFrame" name="frame_7">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_6">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_13">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_7">
           <item>
            <spacer name="horizontalSpacer_5">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>AVG.-Grades</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_6">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <widget class="QFrame" name="frame_6">
           <property name="frameShape">
            <enum>QFrame::Shape::StyledPanel</enum>
           </property>
           <property name="frameShadow">
            <enum>QFrame::Shadow::Raised</enum>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="0" column="2">
     <widget class="QFrame" name="frame_avg_grades_top_left">
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout_11">
       <item row="0" column="0">
        <layout class="QVBoxLayout" name="verticalLayout_11">
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_14">
           <item>
            <spacer name="horizontalSpacer_19">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QLabel" name="label_2">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;</string>
             </property>
             <property name="text">
              <string>AVG.-Grades</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_20">
             <property name="orientation">
              <enum>Qt::Orientation::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <widget class="QFrame" name="frame">
           <property name="frameShape">
            <enum>QFrame::Shape::StyledPanel</enum>
           </property>
           <property name="frameShadow">
            <enum>QFrame::Shadow::Raised</enum>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
    <item row="0" column="4">
     <widget class="QFrame" name="frame_top_right">
      <property name="styleSheet">
       <string notr="true">background-color: rgb(23, 23, 23);</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::Shape::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QGridLayout" name="gridLayout">
       <item row="0" column="0">
        <layout class="QHBoxLayout" name="horizontalLayout_3">
         <item>
          <layout class="QVBoxLayout" name="verticalLayout_5">
           <item alignment="Qt::AlignmentFlag::AlignHCenter|Qt::AlignmentFlag::AlignBottom">
            <widget class="QLabel" name="label_semester_counter_number_left">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>1</string>
             </property>
            </widget>
           </item>
           <item alignment="Qt::AlignmentFlag::AlignHCenter">
            <widget class="QLabel" name="label_semester_counter_text_left">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>Open</string>
             </property>
            </widget>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QVBoxLayout" name="verticalLayout_7">
           <item>
            <widget class="QLabel" name="label_semeseter_counter_text_top">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
</string>
             </property>
             <property name="text">
              <string>Weeks Left</string>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QFrame" name="frame_3">
             <property name="frameShape">
              <enum>QFrame::Shape::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Shadow::Raised</enum>
             </property>
            </widget>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QVBoxLayout" name="verticalLayout_4">
           <item alignment="Qt::AlignmentFlag::AlignHCenter|Qt::AlignmentFlag::AlignBottom">
            <widget class="QLabel" name="label_semester_counter_number_right">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>4</string>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QLabel" name="label_semester_counter_text_right">
             <property name="styleSheet">
              <string notr="true">font: 700 11pt &quot;Graduate&quot;;
color: rgb(51, 255, 0);</string>
             </property>
             <property name="text">
              <string>Done</string>
             </property>
            </widget>
           </item>
          </layout>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>901</width>
     <height>23</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
