Imports System.IO

Module PeopleManagement

    ' Define a Person class
    Public Class Person
        Public Property Name As String
        Public Property Age As Integer
        Public Property Email As String

        Public Sub New(ByVal name As String, ByVal age As Integer, ByVal email As String)
            Me.Name = name
            Me.Age = age
            Me.Email = email
        End Sub

        Public Sub DisplayInfo()
            Console.WriteLine("Name: " & Name)
            Console.WriteLine("Age: " & Age)
            Console.WriteLine("Email: " & Email)
            Console.WriteLine()
        End Sub
    End Class

    ' Path to save and load the data file
    Private Const dataFilePath As String = "people_data.csv"

    ' Main function
    Sub Main()
        Dim people As New List(Of Person)

        ' Load people from the file at the start of the program
        LoadPeopleFromFile(people)

        ' Call the workhorse function to handle the menu
        RunMenu(people)

        Console.WriteLine("Thank you for using the People Management System. Goodbye!")
    End Sub

    ' Workhorse function to handle the menu options
    Sub RunMenu(ByVal people As List(Of Person))
        Dim keepRunning As Boolean = True

        While keepRunning
            DisplayMenu()

            Try
                Dim choice As Integer = Convert.ToInt32(Console.ReadLine())

                Select Case choice
                    Case 1
                        AddPerson(people)
                    Case 2
                        DisplayAllPeople(people)
                    Case 3
                        EditPerson(people)
                    Case 4
                        DeletePerson(people)
                    Case 5
                        SearchPeople(people)
                    Case 6
                        SavePeopleToFile(people)
                    Case 7
                        keepRunning = False
                    Case Else
                        Console.WriteLine("Invalid choice, please try again.")
                End Select

            Catch ex As FormatException
                Console.WriteLine("Invalid input. Please enter a valid number between 1 and 7.")
            Catch ex As Exception
                Console.WriteLine("An unexpected error occurred: " & ex.Message)
            End Try

            Console.WriteLine() ' Adds an extra row for better readability
        End While
    End Sub

    ' Display menu
    Sub DisplayMenu()
        Console.WriteLine("People Management System")
        Console.WriteLine("1. Add a new person")
        Console.WriteLine("2. Display all people")
        Console.WriteLine("3. Edit a person")
        Console.WriteLine("4. Delete a person")
        Console.WriteLine("5. Search people")
        Console.WriteLine("6. Save to file")
        Console.WriteLine("7. Exit")
        Console.Write("Enter your choice (1-7): ")
    End Sub

    ' Function to add a new person
    Sub AddPerson(ByVal people As List(Of Person))
        Try
            Console.Write("Enter name: ")
            Dim name As String = Console.ReadLine().Trim()
            If String.IsNullOrEmpty(name) Then Throw New Exception("Name cannot be empty.")

            Console.Write("Enter age: ")
            Dim age As Integer = Convert.ToInt32(Console.ReadLine())
            If age <= 0 Then Throw New Exception("Age must be a positive number.")

            Console.Write("Enter email: ")
            Dim email As String = Console.ReadLine().Trim()
            If Not IsValidEmail(email) Then Throw New FormatException("The email address format is invalid.")

            Dim newPerson As New Person(name, age, email)
            people.Add(newPerson)

            ' Save the updated list to file
            SavePeopleToFile(people)

            Console.WriteLine("Person added successfully!")

        Catch ex As FormatException
            Console.WriteLine("Invalid input: " & ex.Message)
        Catch ex As Exception
            Console.WriteLine("An error occurred while adding the person: " & ex.Message)
        End Try
    End Sub

    ' Function to display all people
    Sub DisplayAllPeople(ByVal people As List(Of Person))
        Try
            If people.Count = 0 Then
                Console.WriteLine("No people in the list.")
            Else
                For Each person As Person In people
                    person.DisplayInfo()
                Next
            End If
        Catch ex As Exception
            Console.WriteLine("An error occurred while displaying the people: " & ex.Message)
        End Try
    End Sub

    ' Function to edit a person
    Sub EditPerson(ByVal people As List(Of Person))
        Try
            Console.Write("Enter the name of the person to edit: ")
            Dim name As String = Console.ReadLine().Trim()
            Dim person As Person = people.Find(Function(p) p.Name.Equals(name, StringComparison.OrdinalIgnoreCase))

            If person Is Nothing Then
                Console.WriteLine("Person not found.")
                Return
            End If

            Console.Write("Enter new name (leave blank to keep current): ")
            Dim newName As String = Console.ReadLine().Trim()
            If Not String.IsNullOrEmpty(newName) Then person.Name = newName

            Console.Write("Enter new age (leave blank to keep current): ")
            Dim ageInput As String = Console.ReadLine().Trim()
            If Not String.IsNullOrEmpty(ageInput) Then
                Dim newAge As Integer
                If Integer.TryParse(ageInput, newAge) AndAlso newAge > 0 Then
                    person.Age = newAge
                Else
                    Console.WriteLine("Invalid age input, keeping the current age.")
                End If
            End If

            Console.Write("Enter new email (leave blank to keep current): ")
            Dim newEmail As String = Console.ReadLine().Trim()
            If Not String.IsNullOrEmpty(newEmail) Then
                If IsValidEmail(newEmail) Then
                    person.Email = newEmail
                Else
                    Console.WriteLine("Invalid email format, keeping the current email.")
                End If
            End If

            ' Save the updated list to file
            SavePeopleToFile(people)

            Console.WriteLine("Person updated successfully!")

        Catch ex As Exception
            Console.WriteLine("An error occurred while editing the person: " & ex.Message)
        End Try
    End Sub

    ' Function to delete a person
    Sub DeletePerson(ByVal people As List(Of Person))
        Try
            Console.Write("Enter the name of the person to delete: ")
            Dim name As String = Console.ReadLine().Trim()
            Dim person As Person = people.Find(Function(p) p.Name.Equals(name, StringComparison.OrdinalIgnoreCase))

            If person Is Nothing Then
                Console.WriteLine("Person not found.")
                Return
            End If

            Console.Write("Are you sure you want to delete this person? (y/n): ")
            Dim confirmation As String = Console.ReadLine().Trim().ToLower()
            If confirmation = "y" Then
                people.Remove(person)
                SavePeopleToFile(people)
                Console.WriteLine("Person deleted successfully!")
            Else
                Console.WriteLine("Deletion cancelled.")
            End If

        Catch ex As Exception
            Console.WriteLine("An error occurred while deleting the person: " & ex.Message)
        End Try
    End Sub

    ' Function to search for people by name
    Sub SearchPeople(ByVal people As List(Of Person))
        Try
            Console.Write("Enter the name to search: ")
            Dim searchName As String = Console.ReadLine().Trim()
            Dim results As List(Of Person) = people.FindAll(Function(p) p.Name.IndexOf(searchName, StringComparison.OrdinalIgnoreCase) >= 0)

            If results.Count = 0 Then
                Console.WriteLine("No matching people found.")
            Else
                Console.WriteLine("Search results:")
                For Each person As Person In results
                    person.DisplayInfo()
                Next
            End If
        Catch ex As Exception
            Console.WriteLine("An error occurred while searching for people: " & ex.Message)
        End Try
    End Sub

    ' Function to validate email format
    Function IsValidEmail(ByVal email As String) As Boolean
        Try
            Dim addr = New System.Net.Mail.MailAddress(email)
            Return addr.Address = email
        Catch
            Return False
        End Try
    End Function

    ' Function to save people to a file
    Sub SavePeopleToFile(ByVal people As List(Of Person))
        Try
            Using writer As New StreamWriter(dataFilePath)
                For Each person As Person In people
                    writer.WriteLine($"{person.Name},{person.Age},{person.Email}")
                Next
            End Using
            Console.WriteLine("Data saved successfully to 'people_data.csv'.")
        Catch ex As UnauthorizedAccessException
            Console.WriteLine("Error: Access to the file is denied. Please check the file permissions.")
        Catch ex As IOException
            Console.WriteLine("Error: An I/O error occurred while saving the data. Please try again.")
        Catch ex As Exception
            Console.WriteLine("An unexpected error occurred while saving data: " & ex.Message)
        End Try
    End Sub

    ' Function to load people from a file
    Sub LoadPeopleFromFile(ByVal people As List(Of Person))
        Try
            If File.Exists(dataFilePath) Then
                Using reader As New StreamReader(dataFilePath)
                    While Not reader.EndOfStream
                        Dim line As String = reader.ReadLine()
                        Dim parts() As String = line.Split(","c)
                        If parts.Length = 3 Then
                            Dim name As String = parts(0).Trim()
                            Dim age As Integer
                            If Integer.TryParse(parts(1).Trim(), age) AndAlso age > 0 Then
                                Dim email As String = parts(2).Trim()
                                If IsValidEmail(email) Then
                                    people.Add(New Person(name, age, email))
                                Else
                                    Console.WriteLine($"Invalid email format found in file for {name}. Skipping entry.")
                                End If
                            Else
                                Console.WriteLine($"Invalid age found in file for {name}. Skipping entry.")
                            End If
                        Else
                            Console.WriteLine("Malformed line found in file, skipping entry.")
                        End If
                    End While
                End Using
                Console.WriteLine("Data loaded successfully from 'people_data.csv'.")
            End If
        Catch ex As FileNotFoundException
            Console.WriteLine("The data file was not found. A new file will be created when you save data.")
        Catch ex As UnauthorizedAccessException
            Console.WriteLine("Error: Access to the file is denied. Please check the file permissions.")
        Catch ex As IOException
            Console.WriteLine("Error: An I/O error occurred while loading the data. Please try again.")
        Catch ex As Exception
            Console.WriteLine("An unexpected error occurred while loading data: " & ex.Message)
        End Try
    End Sub

End Module
