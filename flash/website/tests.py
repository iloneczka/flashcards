# from django.test import TestCase
# from django.urls import reverse
# from .models import Card


# class CardTests(TestCase):

#     def setUp(self):
#         self.example_card = Card.objects.create(
#             question="Example Question",
#             answer="Example Answer",
#             box=1
#         )

#     def test_add_new_card(self):
#         response = self.client.post(reverse('create_new_card'), {
#             'question': 'New Question',
#             'answer': 'New Answer',
#             'box': 'box1'
#         })
#         # print(response)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Success!')
#         self.assertContains(response, 'You added a new card:')
#         self.assertContains(response, 'Front Card:')
#         self.assertContains(response, 'Back Card:')

#         # Check if the card was added to the database
#         self.assertEqual(Card.objects.count(), 2)
#         card = Card.objects.get(id=2)
#         self.assertEqual(card.question, 'New Question')
#         self.assertEqual(card.answer, 'New Answer')
#         self.assertEqual(card.box, 1)

#     def test_add_new_card_without_front_card(self):
#         response = self.client.post(reverse('create_new_card'), {
#             'answer': 'Answer',
#             'box': 'box1'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertNotContains(response, 'Success!')
#         self.assertNotContains(response, 'You added a new card:')
#         self.assertNotContains(response, 'Front Card:')
#         self.assertNotContains(response, 'Back Card:')

#         # Check if the card was not added to the database
#         self.assertEqual(Card.objects.count(), 1)

#     def test_add_new_card_without_back_card(self):
#         response = self.client.post(reverse('create_new_card'), {
#             'question': 'Question',
#             'box': 'box1'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertNotContains(response, 'Success!')
#         self.assertNotContains(response, 'You added a new card:')
#         self.assertNotContains(response, 'Front Card:')
#         self.assertNotContains(response, 'Back Card:')

#         # Check if the card was not added to the database
#         self.assertEqual(Card.objects.count(), 1)

# # !!!DO POPRAWY
#     # def test_edit_card(self):
#     #     card_id = self.example_card.pk
#     #     response = self.client.post(reverse('edit_card', args=[card_id]), {'question': 'New Question', 'answer': 'New Answer', 'box': 'box2'})
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertJSONEqual(response.content, {'status': 'success'})

#     def test_delete_card(self):
#         card_id = self.example_card.pk
#         response = self.client.post(reverse('delete_card', args=[card_id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {'status': 'success'})
