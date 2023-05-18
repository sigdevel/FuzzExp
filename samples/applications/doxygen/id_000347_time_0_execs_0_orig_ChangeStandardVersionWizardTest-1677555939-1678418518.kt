package ch.hsr.ifs.iltis.cpp.versionator.tests.wizard

import ch.hsr.ifs.iltis.cpp.versionator.definition.CPPVersion
import ch.hsr.ifs.iltis.cpp.versionator.tests.getTableItemById
import ch.hsr.ifs.iltis.cpp.versionator.tests.settle
import org.eclipse.core.resources.ResourcesPlugin
import org.eclipse.swtbot.eclipse.finder.SWTWorkbenchBot
import org.eclipse.swtbot.swt.finder.exceptions.WidgetNotFoundException
import org.eclipse.swtbot.swt.finder.junit.SWTBotJunit4ClassRunner
import org.eclipse.ui.PlatformUI
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.CoreMatchers.equalTo
import org.hamcrest.CoreMatchers.hasItem
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.AfterClass
import org.junit.Assert.fail
import org.junit.Before
import org.junit.BeforeClass
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(SWTBotJunit4ClassRunner::class)
class ChangeStandardVersionWizardTest {

	companion object {

		private const val PERSPECTIVE_ID = "org.eclipse.cdt.ui.CPerspective"

		private const val PROJECT_NAME = "ChangeStandardVersionTestProject"

		private const val COMBO_LABEL = "Set standard version to:"

		lateinit var BOT: SWTWorkbenchBot

		@BeforeClass
		@JvmStatic
		fun setupClass() {
			BOT = SWTWorkbenchBot().apply {
				try {
					viewByTitle("Welcome").close()
				} catch (e: WidgetNotFoundException) {
				}

				with(PlatformUI.getWorkbench()) {
					display.syncExec {
						showPerspective(PERSPECTIVE_ID, activeWorkbenchWindow)
					}
				}

			}
		}

		@AfterClass
		@JvmStatic
		fun tearDownClass() {
			BOT.settle()
		}

	}

	@Before
	fun createProject() {
		with(BOT) {
			menu("File")
				.menu("New")
				.menu("Project...")
				.click()

			shell("New Project")
				.activate()

			tree()
				.expandNode("C/C++")
				.select("C/C++ Project")

			button("Next >")
				.click()

			table()
				.getTableItemById("C++ Managed Build")
				.select()

			button("Next >")
				.click()

			textWithLabel("Project name:")
				.setText(PROJECT_NAME)

			button("Finish")
				.click()

			settle()

			viewByTitle("Project Explorer").show()

			tree().getTreeItem(PROJECT_NAME).select()
		}
	}

	@After
	fun deleteProject() {
		with(BOT) {
			viewByTitle("Project Explorer").show()

			tree().getTreeItem(PROJECT_NAME).select()
				.contextMenu("Delete")
				.click()

			checkBox().click()

			button("OK").click()
		}
	}

	@Test
	fun `Change C++ Standard to C++98`() {
		with(BOT) {
			viewByTitle("Project Explorer").show()

			tree().getTreeItem(PROJECT_NAME).select()
				.contextMenu("Configure")
				.menu("Change C++ Standard")
				.click()

			assertThat(
				comboBoxWithLabel(COMBO_LABEL).items().asIterable(),
				hasItem(`is`(equalTo((CPPVersion.CPP_98.versionString))))
			)

			comboBoxWithLabel(COMBO_LABEL)
				.setSelection(CPPVersion.CPP_98.versionString)
			
			button("Finish")
				.click()
		}

		with(ResourcesPlugin.getWorkspace()) {
			root.getProject(PROJECT_NAME)?.apply {
				assertThat(CPPVersion.getForProject(this), `is`(equalTo(CPPVersion.CPP_98)))
			} ?: fail("Failed to get IProject for name '$PROJECT_NAME'")
		}
	}

}