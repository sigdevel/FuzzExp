package org.jetbrains.kotlin.ui.formatter

import com.intellij.formatting.*
import com.intellij.lang.ASTNode
import com.intellij.openapi.editor.impl.DocumentImpl
import com.intellij.openapi.util.TextRange
import com.intellij.openapi.util.text.StringUtil
import com.intellij.psi.codeStyle.CodeStyleSettings
import com.intellij.psi.codeStyle.CommonCodeStyleSettings.IndentOptions
import com.intellij.psi.formatter.FormatterUtil
import com.intellij.util.text.CharArrayUtil
import org.eclipse.core.resources.IFile
import org.eclipse.jface.text.Document
import org.eclipse.jface.text.IDocument
import org.jetbrains.kotlin.core.model.getEnvironment
import org.jetbrains.kotlin.eclipse.ui.utils.IndenterUtil
import org.jetbrains.kotlin.eclipse.ui.utils.LineEndUtil
import org.jetbrains.kotlin.idea.formatter.KotlinSpacingBuilderUtil
import org.jetbrains.kotlin.idea.formatter.createSpacingBuilder
import org.jetbrains.kotlin.psi.KtFile
import org.jetbrains.kotlin.psi.KtPsiFactory
import com.intellij.openapi.editor.Document as IdeaDocument

fun formatCode(
		source: String,
        fileName: String,
        psiFactory: KtPsiFactory,
        settings: CodeStyleSettings
) = KotlinFormatter(source, fileName, psiFactory, settings).formatCode()


fun reformatAll(
        containingFile: KtFile,
        rootBlock: Block,
        settings: CodeStyleSettings,
        document: IDocument
) {
	formatRange(containingFile, rootBlock, settings, document, containingFile.textRange)
}

fun formatRange(
        document: IDocument,
        range: EclipseDocumentRange,
        psiFactory: KtPsiFactory,
        fileName: String,
        settings: CodeStyleSettings
) {
	formatRange(document, range.toPsiRange(document), psiFactory, fileName, settings)
}

fun formatRange(
        document: IDocument,
        range: TextRange,
        psiFactory: KtPsiFactory,
        fileName: String,
        settings: CodeStyleSettings
) {
	val ktFile = createKtFile(document.get(), psiFactory, fileName)
	val rootBlock = KotlinBlock(ktFile.node,
			NULL_ALIGNMENT_STRATEGY,
			Indent.getNoneIndent(),
			null,
			settings,
			createSpacingBuilder(settings, KotlinSpacingBuilderUtilImpl))

	formatRange(ktFile, rootBlock, settings, document, range)
}

private fun formatRange(
		containingFile: KtFile,
		rootBlock: Block,
		settings: CodeStyleSettings,
		document: IDocument,
		range: TextRange
) {
	val formattingModel = buildModel(containingFile, rootBlock, settings, document, false)

	val ranges = FormatTextRanges(range, true)
	FormatterImpl().format(formattingModel, settings, settings.indentOptions, ranges)
}

fun adjustIndent(containingFile: KtFile, rootBlock: Block,
				 settings: CodeStyleSettings, offset: Int, document: IDocument) {
	val formattingModel = buildModel(containingFile, rootBlock, settings, document, true)
	FormatterImpl().adjustLineIndent(
			formattingModel, settings, settings.indentOptions, offset, getSignificantRange(containingFile, offset))
}

fun getMockDocument(document: IdeaDocument): IdeaDocument {
	return object : IdeaDocument by document {
	}
}

fun initializaSettings(options: IndentOptions) {
	with(options) {
		USE_TAB_CHARACTER = !IndenterUtil.isSpacesForTabs()
		INDENT_SIZE = IndenterUtil.getDefaultIndent()
		TAB_SIZE = IndenterUtil.getDefaultIndent()
	}
}

data class EclipseDocumentRange(val startOffset: Int, val endOffset: Int)

private fun EclipseDocumentRange.toPsiRange(document: IDocument): TextRange {
	val startPsiOffset = LineEndUtil.convertCrToDocumentOffset(document, startOffset)
	val endPsiOffset = LineEndUtil.convertCrToDocumentOffset(document, endOffset)
	return TextRange(startPsiOffset, endPsiOffset)
}

val NULL_ALIGNMENT_STRATEGY = NodeAlignmentStrategy.fromTypes(KotlinAlignmentStrategy.wrap(null))

private fun buildModel(
		containingFile: KtFile,
		rootBlock: Block,
		settings: CodeStyleSettings,
		document: IDocument,
		forLineIndentation: Boolean): EclipseDocumentFormattingModel {
	initializaSettings(settings.indentOptions!!)
	val formattingDocumentModel =
			EclipseFormattingModel(
					DocumentImpl(containingFile.viewProvider.contents, true),
					containingFile,
					settings,
					forLineIndentation)

	return EclipseDocumentFormattingModel(containingFile, rootBlock, formattingDocumentModel, document, settings)
}


private fun getSignificantRange(file: KtFile, offset: Int): TextRange {
	val elementAtOffset = file.findElementAt(offset)
	if (elementAtOffset == null) {
		val significantRangeStart = CharArrayUtil.shiftBackward(file.text, offset - 1, "\r\t ")
		return TextRange(Math.max(significantRangeStart, 0), offset)
	}

	return elementAtOffset.textRange
}


private class KotlinFormatter(
        source: String,
        fileName: String,
        psiFactory: KtPsiFactory,
        val settings: CodeStyleSettings
) {
	val ktFile = createKtFile(source, psiFactory, fileName)

    val sourceDocument = Document(source)

    fun formatCode(): String {
        FormatterImpl()
        val rootBlock = KotlinBlock(ktFile.node,
                NULL_ALIGNMENT_STRATEGY,
                Indent.getNoneIndent(),
                null,
                settings,
                createSpacingBuilder(settings, KotlinSpacingBuilderUtilImpl))

		reformatAll(ktFile, rootBlock, settings, sourceDocument)

		return sourceDocument.get()
	}
}

fun createPsiFactory(eclipseFile: IFile): KtPsiFactory {
	val environment = getEnvironment(eclipseFile)
	return KtPsiFactory(environment.project)
}

fun createKtFile(source: String, psiFactory: KtPsiFactory, fileName: String): KtFile {
	return psiFactory.createFile(fileName, StringUtil.convertLineSeparators(source))
}

private fun createWhitespaces(countSpaces: Int) = IndenterUtil.SPACE_STRING.repeat(countSpaces)

object KotlinSpacingBuilderUtilImpl : KotlinSpacingBuilderUtil {
	override fun createLineFeedDependentSpacing(minSpaces: Int,
												maxSpaces: Int,
												minimumLineFeeds: Int,
												keepLineBreaks: Boolean,
												keepBlankLines: Int,
												dependency: TextRange,
												rule: DependentSpacingRule): Spacing {
		return object : DependantSpacingImpl(minSpaces, maxSpaces, dependency, keepLineBreaks, keepBlankLines, rule) {
		}
	}

	override fun getPreviousNonWhitespaceLeaf(node: ASTNode?): ASTNode? {
		return FormatterUtil.getPreviousNonWhitespaceLeaf(node)
	}

	override fun isWhitespaceOrEmpty(node: ASTNode?): Boolean {
		return FormatterUtil.isWhitespaceOrEmpty(node)
	}
}